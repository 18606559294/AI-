import { useScrollAnimation } from '../../hooks/useScrollAnimation';

const steps = [
  {
    num: '1',
    title: '注册 / 登录',
    desc: '30 秒完成注册，立即开始创建你的专业简历。支持邮箱和第三方登录。',
  },
  {
    num: '2',
    title: 'AI 生成 / 编辑',
    desc: '输入基本信息，AI 自动生成简历初稿。选择模板，自定义编辑内容，实时预览效果。',
  },
  {
    num: '3',
    title: '导出 / 投递',
    desc: '一键导出 PDF、Word 或 HTML 格式。直接投递，让 HR 眼前一亮。',
  },
];

export default function HowItWorksSection() {
  const { ref, isVisible } = useScrollAnimation();

  return (
    <section className="lp-how">
      <div className="lp-container">
        <div className="lp-section-header">
          <div className="lp-section-badge">使用流程</div>
          <h2 className="lp-section-title">三步搞定完美简历</h2>
          <p className="lp-section-subtitle">简单三步，从零到投递</p>
        </div>
        <div
          ref={ref}
          className="lp-steps"
          style={{
            opacity: isVisible ? 1 : 0,
            transform: isVisible ? 'translateY(0)' : 'translateY(30px)',
            transition: 'opacity 0.6s ease, transform 0.6s ease',
          }}
        >
          {steps.map((s) => (
            <div key={s.num} className="lp-step">
              <div className="lp-step-number">{s.num}</div>
              <h3 className="lp-step-title">{s.title}</h3>
              <p className="lp-step-desc">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
