/// <reference path="./.sst/platform/config.d.ts" />

import * as gcp from "@pulumi/gcp";

export default $config({
  app(input) {
    return {
      name: "fastapi-demo",
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws", // SST lưu trạng thái tại AWS hoặc Cloudflare
    };
  },
  async run() {
    console.log(`Đang triển khai môi trường (stage): ${$app.stage}`);

    // 1. Chỉ định Image Docker mà ta đã push lên Artifact Registry ở Ngày 3 & 4
    const imageUrl = "asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-demo/fastapi-demo-project:latest";

    // 2. Khai báo dịch vụ Cloud Run
    const service = new gcp.cloudrun.Service(`fastapi-service-${$app.stage}`, {
      location: "asia-southeast1",
      template: {
        spec: {
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

    // 4. Xuất URL của trang web ra màn hình sau khi Deploy xong
    return {
      WebsiteURL: service.statuses[0].url,
    };
  },
});
