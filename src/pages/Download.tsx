import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import { FileText, Code, BookOpen, Monitor, Apple, Server, Terminal, ArrowDownToLine } from "lucide-react";

const downloadItems = [
  {
    title: "ORV IDE",
    description: "集成开发环境，支持代码编辑、调试和烧录",
    icon: Code,
    platforms: [
      { name: "Windows", icon: Monitor, link: "#" },
      { name: "macOS", icon: Apple, link: "#" },
      { name: "Linux", icon: Server, link: "#" },
    ],
    version: "v2.1.0",
    date: "2024-01-15",
  },
  {
    title: "固件",
    description: "最新的设备固件和 bootloader",
    icon: Terminal,
    platforms: [
      { name: "ORV-Cam Pro", icon: Monitor, link: "#" },
      { name: "ORV-Cam Lite", icon: Monitor, link: "#" },
      { name: "ORV-Controller", icon: Monitor, link: "#" },
    ],
    version: "v1.8.2",
    date: "2024-01-10",
  },
];

const documentation = [
  { title: "快速入门", description: "5 分钟上手指南", icon: BookOpen },
  { title: "API 参考", description: "完整的函数和类说明", icon: Code },
  { title: "教程", description: "从入门到精通的教程", icon: FileText },
  { title: "硬件规格", description: "详细的硬件参数文档", icon: Terminal },
];

export default function DownloadPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200">
      <Navbar />

      <section className="py-20">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-5xl font-display font-bold text-white mb-4">
              下载中心
            </h1>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              获取最新的开发工具、固件和文档资源
            </p>
          </div>

          <div className="mb-20">
            <h2 className="text-3xl font-display font-bold text-white mb-10 flex items-center gap-3">
              <ArrowDownToLine className="w-8 h-8 text-accent-500" />
              软件下载
            </h2>
            <div className="space-y-6">
              {downloadItems.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <div
                    key={idx}
                    className="bg-slate-900 border border-slate-800 rounded-2xl p-8 hover:border-primary-500/50 transition-all"
                  >
                    <div className="md:flex items-start gap-8">
                      <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-accent-600 rounded-xl flex items-center justify-center flex-shrink-0 mb-6 md:mb-0">
                        <Icon className="w-8 h-8 text-white" />
                      </div>
                      <div className="flex-grow">
                        <div className="flex flex-wrap items-center gap-4 mb-2">
                          <h3 className="text-2xl font-semibold text-white">
                            {item.title}
                          </h3>
                          <span className="px-3 py-1 bg-accent-900/50 text-accent-400 text-sm rounded-full">
                            {item.version}
                          </span>
                          <span className="text-slate-500 text-sm">
                            {item.date}
                          </span>
                        </div>
                        <p className="text-slate-400 mb-6">{item.description}</p>
                        <div className="flex flex-wrap gap-4">
                          {item.platforms.map((platform, pIdx) => {
                            const PlatformIcon = platform.icon;
                            return (
                              <a
                                key={pIdx}
                                href={platform.link}
                                className="inline-flex items-center gap-2 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white font-medium rounded-lg transition-all border border-slate-700 hover:border-accent-500/50"
                              >
                                <PlatformIcon className="w-5 h-5" />
                                {platform.name}
                              </a>
                            );
                          })}
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="mb-20">
            <h2 className="text-3xl font-display font-bold text-white mb-10 flex items-center gap-3">
              <FileText className="w-8 h-8 text-primary-500" />
              文档资源
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {documentation.map((doc, idx) => {
                const Icon = doc.icon;
                return (
                  <a
                    key={idx}
                    href="#"
                    className="bg-slate-900 border border-slate-800 rounded-xl p-8 hover:border-accent-500/50 transition-all group"
                  >
                    <div className="w-14 h-14 bg-primary-900/50 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <Icon className="w-7 h-7 text-primary-400" />
                    </div>
                    <h3 className="text-xl font-semibold text-white mb-2">
                      {doc.title}
                    </h3>
                    <p className="text-slate-400 text-sm">{doc.description}</p>
                  </a>
                );
              })}
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">
            <h3 className="text-2xl font-display font-bold text-white mb-6">
              需要帮助？
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-12 h-12 bg-accent-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BookOpen className="w-6 h-6 text-accent-400" />
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">查看文档</h4>
                <p className="text-slate-400 text-sm">
                  详细的文档和示例代码
                </p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-primary-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Code className="w-6 h-6 text-primary-400" />
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">GitHub</h4>
                <p className="text-slate-400 text-sm">
                  源代码和问题反馈
                </p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-accent-900/50 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Terminal className="w-6 h-6 text-accent-400" />
                </div>
                <h4 className="text-lg font-semibold text-white mb-2">社区论坛</h4>
                <p className="text-slate-400 text-sm">
                  与其他开发者交流
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
