import { Link } from "react-router-dom";
import { Eye, Zap, Layers, Cpu, ArrowRight, Camera, Gamepad2, MonitorPlay } from "lucide-react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";

const features = [
  {
    icon: Eye,
    title: "视觉模块",
    description: "高性能机器视觉处理，支持多种传感器和算法",
  },
  {
    icon: Zap,
    title: "自动化外设控制",
    description: "精准控制电机、舵机和各类执行器",
  },
  {
    icon: Layers,
    title: "应用仿真",
    description: "完整的仿真环境，加速开发调试流程",
  },
];

const products = [
  {
    name: "ORV-Cam Pro",
    description: "高性能视觉处理模块，4K 分辨率，实时 AI 推理",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20robot%20vision%20camera%20module%20on%20dark%20background&image_size=square",
    price: "¥1,299",
  },
  {
    name: "ORV-Controller",
    description: "多功能外设控制器，支持 16 路 PWM 和 CAN 总线",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=electronic%20circuit%20board%20microcontroller%20robot%20controller&image_size=square",
    price: "¥899",
  },
  {
    name: "ORV-Starter Kit",
    description: "完整入门套件，包含视觉模块、控制器和配件",
    image: "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=robotics%20electronics%20kit%20components%20package&image_size=square",
    price: "¥2,499",
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <Navbar />

      <section className="relative overflow-hidden py-24">
        <div className="absolute inset-0 bg-gradient-to-b from-primary-950/50 to-slate-950" />
        <div className="container mx-auto relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-accent-950/50 border border-accent-800 rounded-full text-accent-400 text-sm mb-8">
              <span className="w-2 h-2 bg-accent-500 rounded-full animate-pulse" />
              开源 · 免费 · 强大
            </div>
            <h1 className="text-5xl md:text-7xl font-display font-bold text-white mb-6 leading-tight">
              下一代
              <span className="bg-gradient-to-r from-accent-400 via-primary-500 to-accent-400 bg-clip-text text-transparent">
                机器人视觉平台
              </span>
            </h1>
            <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto">
              提供完整的自动化外设控制、视觉模块和应用仿真调试工具，让机器人开发更简单高效。
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/download"
                className="px-8 py-4 bg-gradient-to-r from-primary-600 to-accent-600 hover:from-primary-500 hover:to-accent-500 text-white font-semibold rounded-lg transition-all hover:shadow-lg hover:shadow-primary-500/25 flex items-center justify-center gap-2"
              >
                开始下载
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                to="/products"
                className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white font-semibold rounded-lg transition-all border border-slate-700"
              >
                查看产品
              </Link>
            </div>
          </div>

          <div className="mt-20 grid md:grid-cols-3 gap-8">
            {features.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <div
                  key={idx}
                  className="bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-xl p-8 hover:border-accent-500/50 transition-all hover:shadow-xl hover:shadow-accent-500/10 group"
                >
                  <div className="w-14 h-14 bg-gradient-to-br from-primary-600 to-accent-600 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                    <Icon className="w-7 h-7 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-slate-400">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      <section className="py-20">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-display font-bold text-white mb-4">
              核心产品
            </h2>
            <p className="text-slate-400 text-lg">
              精心设计的硬件模块，满足各种应用场景需求
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {products.map((product, idx) => (
              <div
                key={idx}
                className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden hover:border-primary-500/50 transition-all group"
              >
                <div className="aspect-square bg-slate-800 overflow-hidden">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-white mb-2">
                    {product.name}
                  </h3>
                  <p className="text-slate-400 text-sm mb-4">
                    {product.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-bold text-accent-400">
                      {product.price}
                    </span>
                    <Link
                      to="/products"
                      className="text-primary-400 hover:text-primary-300 font-medium flex items-center gap-1"
                    >
                      了解更多
                      <ArrowRight className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 bg-slate-900/50">
        <div className="container mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-display font-bold text-white mb-6">
                强大的开发工具链
              </h2>
              <div className="space-y-6">
                <div className="flex gap-4">
                  <div className="w-12 h-12 bg-primary-900/50 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Camera className="w-6 h-6 text-primary-400" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-1">
                      视觉处理
                    </h4>
                    <p className="text-slate-400">
                      内置多种计算机视觉算法，支持目标检测、图像识别、视觉追踪
                    </p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="w-12 h-12 bg-accent-900/50 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Gamepad2 className="w-6 h-6 text-accent-400" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-1">
                      外设控制
                    </h4>
                    <p className="text-slate-400">
                      统一的控制接口，支持多种外设协议和通信方式
                    </p>
                  </div>
                </div>
                <div className="flex gap-4">
                  <div className="w-12 h-12 bg-primary-900/50 rounded-lg flex items-center justify-center flex-shrink-0">
                    <MonitorPlay className="w-6 h-6 text-primary-400" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-1">
                      仿真调试
                    </h4>
                    <p className="text-slate-400">
                      集成仿真环境，无需硬件即可快速验证算法和逻辑
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-slate-800 rounded-2xl p-8 border border-slate-700">
              <div className="aspect-video bg-slate-900 rounded-xl flex items-center justify-center">
                <div className="text-center">
                  <Cpu className="w-16 h-16 text-accent-500 mx-auto mb-4" />
                  <p className="text-slate-400">仿真环境预览</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20">
        <div className="container mx-auto">
          <div className="bg-gradient-to-r from-primary-900 to-accent-900 rounded-3xl p-12 text-center">
            <h2 className="text-4xl font-display font-bold text-white mb-4">
              准备好开始了吗？
            </h2>
            <p className="text-slate-300 text-lg mb-8 max-w-2xl mx-auto">
              下载我们的开发工具，探索机器人视觉的无限可能
            </p>
            <Link
              to="/download"
              className="inline-flex items-center gap-2 px-8 py-4 bg-white text-slate-900 font-semibold rounded-lg hover:bg-slate-100 transition-all"
            >
              立即下载
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
