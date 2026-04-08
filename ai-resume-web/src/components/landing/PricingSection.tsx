import { Link } from 'react-router-dom';
import { useScrollAnimation } from '../../hooks/useScrollAnimation';

const Check = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" width="18" height="18">
    <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 12.75 6 6 9-13.5" />
  </svg>
);

export default function PricingSection() {
  const { ref, isVisible } = useScrollAnimation();

  return (
    <section className="lp-pricing">
      <div className="lp-container">
        <div className="lp-section-header">
          <div className="lp-section-badge">定价方案</div>
          <h2 className="lp-section-title">简单透明的定价</h2>
          <p className="lp-section-subtitle">免费开始，按需升级</p>
        </div>
        <div
          ref={ref}
          className="lp-pricing-grid"
          style={{
            opacity: isVisible ? 1 : 0,
            transform: isVisible ? 'translateY(0)' : 'translateY(30px)',
            transition: 'opacity 0.6s ease, transform 0.6s ease',
          }}
        >
          {/* Free */}
          <div className="lp-pricing-card">
            <h3 className="lp-pricing-name">免费版</h3>
            <div className="lp-pricing-price">
              ¥0<span> / 永久</span>
            </div>
            <p className="lp-pricing-desc">适合初次使用，体验核心功能</p>
            <ul className="lp-pricing-features">
              <li><Check />3 份简历</li>
              <li><Check />20+ 基础模板</li>
              <li><Check />PDF 导出</li>
              <li><Check />AI 基础优化建议</li>
              <li><Check />在线编辑器</li>
            </ul>
            <Link to="/register" className="lp-pricing-btn outline">免费开始</Link>
          </div>

          {/* Pro */}
          <div className="lp-pricing-card featured">
            <h3 className="lp-pricing-name">专业版</h3>
            <div className="lp-pricing-price">
              ¥29<span> / 月</span>
            </div>
            <p className="lp-pricing-desc">求职冲刺期，解锁全部能力</p>
            <ul className="lp-pricing-features">
              <li><Check />无限简历</li>
              <li><Check />200+ 全部模板</li>
              <li><Check />PDF + Word + HTML 导出</li>
              <li><Check />AI 深度优化 & 模拟面试</li>
              <li><Check />ATS 系统兼容检测</li>
              <li><Check />多端同步 (Web/桌面/手机)</li>
              <li><Check />优先客服支持</li>
            </ul>
            <Link to="/register" className="lp-pricing-btn primary">立即升级</Link>
          </div>
        </div>
      </div>
    </section>
  );
}
