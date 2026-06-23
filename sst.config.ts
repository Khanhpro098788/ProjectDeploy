/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "fastapi-demo",
      // Chiến lược giữ lại tài nguyên:
      // - Nếu là môi trường production: Giữ lại tài nguyên (retain) để tránh xóa nhầm dữ liệu
      // - Nếu là môi trường dev/staging: Xóa sạch (remove) khi chạy sst remove để tiết kiệm tiền
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws",
    };
  },
  async run() {
    // ---------------------------------------------------------
    // Định nghĩa Cơ sở hạ tầng (Infrastructure) tại đây
    // Dưới đây là ví dụ khai báo một dịch vụ (Service)
    // ---------------------------------------------------------
    
    // In ra môi trường hiện tại đang chạy (dev, staging, hoặc prod)
    console.log(`Đang triển khai môi trường (stage): ${$app.stage}`);
    
    // (Trong các bài tiếp theo, chúng ta sẽ viết code tạo Cloud Run hoặc VPC tại đây)
  },
});
