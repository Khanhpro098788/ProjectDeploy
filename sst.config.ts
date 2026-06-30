/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "fastapi-demo",
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws", // SST lưu trạng thái tại AWS S3
      providers: {
        gcp: "9.28.0", // Khai báo chính xác phiên bản GCP Provider
      },
    };
  },
  async run() {
    const gcp = await import("@pulumi/gcp");
    const pulumi = await import("@pulumi/pulumi");
    console.log(`Đang triển khai môi trường (stage): ${$app.stage}`);

    // 1. Chỉ định Image Docker mà ta đã push lên Artifact Registry ở Ngày 3 & 4
    const imageUrl = process.env.IMAGE_URL || "asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-demo/fastapi-demo-project:048348536c6d0d6b52ade025b00957d98f9d9e78";

    // 2. Khai báo dịch vụ Cloud Run
    const service = new gcp.cloudrun.Service(`fastapi-service-${$app.stage}`, {
      location: "asia-southeast1",
      template: {
        spec: {
          serviceAccountName: "cloudrun-runtime-sa@khanh-fastapi-deploy-937.iam.gserviceaccount.com",
          containers: [{
            image: imageUrl,
            ports: [{ containerPort: 8080 }],
          }],
        },
      },
    });

    // 3. Mở quyền truy cập công khai (Allow unauthenticated)
    new gcp.cloudrun.IamMember(`public-access-${$app.stage}`, {
      service: service.name,
      location: service.location,
      role: "roles/run.invoker",
      member: "allUsers",
    });
    const emailChannel = new gcp.monitoring.NotificationChannel(`email-channel-${$app.stage}`, {
      displayName: `Email Alerts - ${$app.stage}`,
      type: "email", // Bắt buộc phải là "email" cho kênh gửi mail
      labels: {
        email_address: "vovankhanh937@gmail.com", // Email thật của em để test
      },
      description: "Email channel for sending infrastructure alerts",
    });
    const alert5xx = new gcp.monitoring.AlertPolicy(`alert-5xx-${$app.stage}`, {
      displayName: `HTTP 5xx Error Alert - ${$app.stage}`,
      combiner: "OR",
      conditions: [{
        displayName: "HTTP 5xx Error Condition",
        conditionThreshold: {
          // Sử dụng pulumi.interpolate để truyền động service.name
          filter: pulumi.interpolate`resource.type = "cloud_run_revision" AND resource.labels.service_name = "${service.name}" AND metric.type = "run.googleapis.com/request_count" AND metric.labels.response_code_class = "5xx"`,
          duration: "60s",
          comparison: "COMPARISON_GT",
          thresholdValue: 0,
          aggregations: [{
            alignmentPeriod: "60s",
            perSeriesAligner: "ALIGN_SUM",
          }],
        },
      }],
      // Liên kết với email channel đã tạo ở trên
      notificationChannels: [emailChannel.name],
      documentation: {
        content: `Hệ thống gặp lỗi 5xx vượt quá ngưỡng cho phép. 
Vui lòng làm theo hướng dẫn tại Runbook sau để xử lý sự cố:
https://github.com/Khanhpro098788/ProjectDeploy/blob/main/docs/runbooks/alert_5xx.md`,
        mimeType: "text/markdown",
      },
    });
    const alertLatency = new gcp.monitoring.AlertPolicy(`alert-latency-${$app.stage}`, {
      displayName: `HTTP Latency Alert - ${$app.stage}`,
      combiner: "OR",
      conditions: [{
        displayName: "HTTP p95 Latency Condition",
        conditionThreshold: {
          filter: pulumi.interpolate`resource.type = "cloud_run_revision" AND resource.labels.service_name = "${service.name}" AND metric.type = "run.googleapis.com/request_latencies"`,
          duration: "300s", // Phải vượt ngưỡng liên tục trong 5 phút
          comparison: "COMPARISON_GT",
          thresholdValue: 2000, // 2000 ms = 2 giây
          aggregations: [{
            alignmentPeriod: "60s",
            perSeriesAligner: "ALIGN_PERCENTILE_95", // Tính phân vị p95
          }],
        },
      }],
      notificationChannels: [emailChannel.name],
    });
    const dashboard = new gcp.monitoring.Dashboard(`dashboard-${$app.stage}`, {
      dashboardJson: pulumi.all([service.name]).apply(([serviceName]) => JSON.stringify({
        displayName: `FastAPI Performance Dashboard - ${$app.stage}`,
        gridLayout: {
          widgets: [
            {
              title: "Request Count (Traffic)",
              xyChart: {
                dataSets: [{
                  timeSeriesQuery: {
                    timeSeriesFilter: {
                      filter: `resource.type="cloud_run_revision" AND resource.labels.service_name="${serviceName}" AND metric.type="run.googleapis.com/request_count"`,
                    }
                  }
                }]
              }
            },
            {
              title: "Latency p95 (Performance)",
              xyChart: {
                dataSets: [{
                  timeSeriesQuery: {
                    timeSeriesFilter: {
                      filter: `resource.type="cloud_run_revision" AND resource.labels.service_name="${serviceName}" AND metric.type="run.googleapis.com/request_latencies"`,
                      aggregation: {
                        perSeriesAligner: "ALIGN_PERCENTILE_95",
                        alignmentPeriod: "60s"
                      }
                    }
                  }
                }]
              }
            }
          ]
        }
      }))
    });
    // 4. Xuất URL của trang web ra màn hình sau khi Deploy xong
    return {
      WebsiteURL: service.statuses.apply(statuses => statuses[0]?.url || "Pending URL"),
      NotificationChannelName: emailChannel.name, // Xuất tên resource dạng ID của GCP
      AlertPolicyName: alert5xx.name,
      AlertLatencyPolicyName: alertLatency.name,
      DashboardName: dashboard.id,
    };
  },
});
