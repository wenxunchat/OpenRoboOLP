import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { Check, ArrowRight, Camera, Cpu, Zap, Box, Users, GraduationCap, Headphones, Globe, TrendingUp, ShieldCheck } from "lucide-react";

const products = [
  {
    category: "视觉模块",
    items: [
      {
        name: "ORV-Cam Pro",
        description: "高性能视觉处理模块，4K 分辨率，实时 AI 推理",
        image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20robot%20vision%20camera%20module%20on%20dark%20background&image_size=square",
        price: "¥1,299",
        specs: ["4K@30fps", "AI 加速", "双 MIPI 接口", "PoE 支持"],
      },
      {
        name: "ORV-Cam Lite",
        description: "轻量化视觉模块，适合入门和教育场景",
        image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=compact%20camera%20module%20electronics&image_size=square",
        price: "¥599",
        specs: ["1080p@60fps", "基础算法", "USB 接口", "低功耗"],
      },
    ],
  },
  {
    category: "外设控制器",
    items: [
      {
        name: "ORV-Controller",
        description: "多功能外设控制器，支持 16 路 PWM 和 CAN 总线",
        image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=electronic%20circuit%20board%20microcontroller%20robot%20controller&image_size=square",
        price: "¥899",
        specs: ["16 路 PWM", "CAN 2.0", "RS485", "6 轴 IMU"],
      },
      {
        name: "ORV-Motor Driver",
        description: "专业电机驱动模块，支持步进和伺服电机",
        image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=motor%20driver%20circuit%20board%20electronics&image_size=square",
        price: "¥499",
        specs: ["4 路驱动", "10A/路", "编码器接口", "过流保护"],
      },
    ],
  },
  {
    category: "套件",
    items: [
      {
        name: "ORV-Starter Kit",
        description: "完整入门套件，包含视觉模块、控制器和配件",
        image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=robotics%20electronics%20kit%20components%20package&image_size=square",
        price: "¥2,499",
        specs: ["ORV-Cam Pro", "ORV-Controller", "配件套装", "完整教程"],
      },
      {
        name: "ORV-Edu Kit",
        description: "教育专用套件，适合教学和实验",
        image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=educational%20robotics%20kit%20learning%20tools&image_size=square",
        price: "¥1,799",
        specs: ["ORV-Cam Lite", "基础控制器", "实验配件", "课程资料"],
      },
    ],
  },
];

export default function Products() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <Navbar />

      <section className="py-20">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-5xl font-display font-bold text-white mb-4">
              产品系列
            </h1>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              从入门级到专业级，为您提供完整的机器人视觉解决方案
            </p>
          </div>

          {products.map((category, catIdx) => (
            <div key={catIdx} className="mb-20">
              <h2 className="text-3xl font-display font-bold text-white mb-10 flex items-center gap-3">
                {catIdx === 0 && <Camera className="w-8 h-8 text-accent-500" />}
                {catIdx === 1 && <Cpu className="w-8 h-8 text-primary-500" />}
                {catIdx === 2 && <Box className="w-8 h-8 text-accent-400" />}
                {category.category}
              </h2>
              <div className="grid md:grid-cols-2 gap-8">
                {category.items.map((product, prodIdx) => (
                  <div
                    key={prodIdx}
                    className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden hover:border-primary-500/50 transition-all group"
                  >
                    <div className="md:flex">
                      <div className="md:w-1/2 aspect-square md:aspect-auto bg-slate-800">
                        <img
                          src={product.image}
                          alt={product.name}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        />
                      </div>
                      <div className="md:w-1/2 p-8 flex flex-col">
                        <h3 className="text-2xl font-semibold text-white mb-2">
                          {product.name}
                        </h3>
                        <p className="text-slate-400 mb-6 flex-grow">
                          {product.description}
                        </p>
                        <ul className="space-y-2 mb-6">
                          {product.specs.map((spec, specIdx) => (
                            <li
                              key={specIdx}
                              className="flex items-center gap-2 text-slate-300"
                            >
                              <Check className="w-4 h-4 text-accent-500 flex-shrink-0" />
                              <span className="text-sm">{spec}</span>
                            </li>
                          ))}
                        </ul>
                        <div className="flex items-center justify-between">
                          <span className="text-3xl font-bold text-accent-400">
                            {product.price}
                          </span>
                          <button className="px-6 py-3 bg-gradient-to-r from-primary-600 to-accent-600 hover:from-primary-500 hover:to-accent-500 text-white font-semibold rounded-lg transition-all flex items-center gap-2">
                            立即购买
                            <ArrowRight className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="py-20 bg-slate-900/50">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-display font-bold text-white mb-4">
              为什么选择 OpenRobotVision？
            </h2>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8">
              <Zap className="w-12 h-12 text-accent-500 mb-6" />
              <h3 className="text-xl font-semibold text-white mb-3">开源开放</h3>
              <p className="text-slate-400">
                完全开源的硬件和软件设计，社区驱动的生态系统
              </p>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8">
              <Cpu className="w-12 h-12 text-primary-500 mb-6" />
              <h3 className="text-xl font-semibold text-white mb-3">高性能</h3>
              <p className="text-slate-400">
                优化的硬件设计，支持实时 AI 推理和高速数据处理
              </p>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8">
              <Box className="w-12 h-12 text-accent-400 mb-6" />
              <h3 className="text-xl font-semibold text-white mb-3">易用性</h3>
              <p className="text-slate-400">
                简洁的 API 设计，丰富的文档和示例，快速上手
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-display font-bold text-white mb-4">
              我们的服务
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              专业的技术支持与服务，助力您的机器人项目取得成功
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-accent-500/50 transition-all group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <GraduationCap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-white mb-3">技术培训</h3>
              <p className="text-slate-400 mb-6">
                提供专业的机器人视觉与自动化控制培训课程，从入门到精通，帮助团队快速上手。
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>现场培训服务</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>在线学习平台</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>定制化课程</span>
                </li>
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-accent-500/50 transition-all group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Headphones className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-white mb-3">技术支持</h3>
              <p className="text-slate-400 mb-6">
                专业的技术支持团队，提供 7x24 小时在线服务，随时解决您的问题。
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>在线技术咨询</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>远程调试支持</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>问题快速响应</span>
                </li>
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-accent-500/50 transition-all group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Users className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-white mb-3">定制开发</h3>
              <p className="text-slate-400 mb-6">
                根据您的需求提供定制化的软硬件解决方案，为您的项目量身定制。
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>硬件定制</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>软件开发</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>算法优化</span>
                </li>
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-accent-500/50 transition-all group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <Globe className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-white mb-3">云服务</h3>
              <p className="text-slate-400 mb-6">
                提供云端数据存储、分析和远程管理服务，让您的机器人更加智能。
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>数据云端存储</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>远程设备管理</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>大数据分析</span>
                </li>
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-accent-500/50 transition-all group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <TrendingUp className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-white mb-3">咨询服务</h3>
              <p className="text-slate-400 mb-6">
                专业的机器人视觉应用咨询，帮助您规划和实施最佳的解决方案。
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>技术方案评估</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>项目可行性分析</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>成本效益分析</span>
                </li>
              </ul>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-accent-500/50 transition-all group">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                <ShieldCheck className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-white mb-3">维护服务</h3>
              <p className="text-slate-400 mb-6">
                定期的设备维护与升级服务，确保您的机器人系统始终保持最佳状态。
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>定期巡检</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>固件升级</span>
                </li>
                <li className="flex items-center gap-2 text-slate-300">
                  <Check className="w-5 h-5 text-accent-500" />
                  <span>故障修复</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 bg-slate-900/50">
        <div className="container mx-auto">
          <div className="bg-gradient-to-r from-primary-900 to-accent-900 rounded-3xl p-12 text-center">
            <h2 className="text-4xl font-display font-bold text-white mb-4">
              准备开始您的机器人项目？
            </h2>
            <p className="text-slate-300 text-xl mb-8 max-w-2xl mx-auto">
              联系我们的专业团队，获取免费的技术咨询和方案评估
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-8 py-4 bg-white text-slate-900 font-semibold rounded-lg hover:bg-slate-100 transition-all flex items-center justify-center gap-2">
                立即咨询
                <ArrowRight className="w-5 h-5" />
              </button>
              <button className="px-8 py-4 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white/10 transition-all">
                查看案例
              </button>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
