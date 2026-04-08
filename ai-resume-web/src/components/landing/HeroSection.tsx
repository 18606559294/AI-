import { Link } from 'react-router-dom';

const Arrow = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" width="18" height="18">
    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
  </svg>
);

const Sparkle = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" width="16" height="16">
    <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456Z" />
  </svg>
);

export default function HeroSection() {
  return (
    <section className="lp-hero">
      <div className="lp-hero-bg" />
      <div className="lp-hero-content">
        <div className="lp-hero-badge">
          <Sparkle />
          AI 驱动 · 智能简历生成平台
        </div>

        <h1 className="lp-hero-title">
          AI 赋能，<br />
          <span className="gradient-text">简历重生</span>
        </h1>

        <p className="lp-hero-subtitle">
          200+ 专业模板 · AI 智能优化排版 · 一键导出 PDF/Word
          <br />
          让每一份简历都成为你的职场敲门砖
        </p>

        <div className="lp-hero-actions">
          <Link to="/login" className="lp-btn-primary">
            免费开始制作 <Arrow />
          </Link>
          <Link to="/templates" className="lp-btn-secondary">
            浏览模板
          </Link>
        </div>

        <div className="lp-hero-stats">
          <div className="lp-hero-stat">
            <div className="lp-hero-stat-value">10,000+</div>
            <div className="lp-hero-stat-label">活跃用户</div>
          </div>
          <div className="lp-hero-stat">
            <div className="lp-hero-stat-value">50,000+</div>
            <div className="lp-hero-stat-label">简历生成</div>
          </div>
          <div className="lp-hero-stat">
            <div className="lp-hero-stat-value">99.2%</div>
            <div className="lp-hero-stat-label">用户好评</div>
          </div>
          <div className="lp-hero-stat">
            <div className="lp-hero-stat-value">200+</div>
            <div className="lp-hero-stat-label">精美模板</div>
          </div>
        </div>
      </div>
    </section>
  );
}
