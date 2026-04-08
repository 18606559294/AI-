import { useStaggerAnimation } from '../../hooks/useScrollAnimation';

const testimonials = [
  {
    name: '张小明',
    role: '应届生 · 成功入职字节跳动',
    text: '用 AI 简历生成器做了第一份简历，没想到面试邀请率这么高！模板很专业，AI 优化建议特别有用。',
    color: '#f59e0b',
  },
  {
    name: '李思思',
    role: '产品经理 · 成功跳槽阿里',
    text: '从模板选择到 AI 优化，整个流程非常顺畅。导出的 PDF 格式完美，直接投递拿到了理想 offer。',
    color: '#10b981',
  },
  {
    name: '王大伟',
    role: '高级工程师 · 成功入职腾讯',
    text: '作为技术人员，之前做的简历太朴素了。用了这个平台后，简历专业度提升了一个档次，强烈推荐！',
    color: '#38bdf8',
  },
];

export default function TestimonialsSection() {
  const { containerRef, visibleItems } = useStaggerAnimation(testimonials.length, 150);

  return (
    <section className="lp-testimonials">
      <div className="lp-container">
        <div className="lp-section-header">
          <div className="lp-section-badge">用户评价</div>
          <h2 className="lp-section-title">他们都在用</h2>
          <p className="lp-section-subtitle">听听成功拿到 offer 的用户怎么说</p>
        </div>
        <div className="lp-testimonials-grid" ref={containerRef}>
          {testimonials.map((t, i) => (
            <div
              key={t.name}
              className="lp-testimonial-card"
              style={{
                opacity: visibleItems.has(i) ? 1 : 0,
                transform: visibleItems.has(i) ? 'translateY(0)' : 'translateY(30px)',
                transition: `opacity 0.5s ease ${i * 0.15}s, transform 0.5s ease ${i * 0.15}s`,
              }}
            >
              <div className="lp-testimonial-stars">★★★★★</div>
              <p className="lp-testimonial-text">"{t.text}"</p>
              <div className="lp-testimonial-author">
                <div className="lp-testimonial-avatar" style={{ background: `${t.color}22`, color: t.color }}>
                  {t.name[0]}
                </div>
                <div>
                  <div className="lp-testimonial-name">{t.name}</div>
                  <div className="lp-testimonial-role">{t.role}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
