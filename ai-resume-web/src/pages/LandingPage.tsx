import { Link } from 'react-router-dom';
import { SEO } from '../components/SEO';
import Navbar from '../components/landing/Navbar';
import HeroSection from '../components/landing/HeroSection';
import StatsSection from '../components/landing/StatsSection';
import FeaturesSection from '../components/landing/FeaturesSection';
import HowItWorksSection from '../components/landing/HowItWorksSection';
import TestimonialsSection from '../components/landing/TestimonialsSection';
import PricingSection from '../components/landing/PricingSection';
import DownloadSection from '../components/landing/DownloadSection';
import FAQSection from '../components/landing/FAQSection';
import Footer from '../components/landing/Footer';
import './LandingPage.css';

function CTASection() {
  return (
    <section className="lp-cta">
      <div className="lp-container">
        <div className="lp-cta-box">
          <h2 className="lp-cta-title">
            准备好制作你的<span style={{ color: 'var(--lp-accent)' }}>完美简历</span>了吗？
          </h2>
          <p className="lp-cta-desc">
            加入 10,000+ 用户，用 AI 生成专业简历，开启你的职场新篇章
          </p>
          <div style={{ position: 'relative', display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/register" className="lp-btn-primary">
              免费注册，立即开始
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" width="18" height="18"><path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" /></svg>
            </Link>
            <Link to="/login" className="lp-btn-secondary">已有账号，登录</Link>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function LandingPage() {
  return (
    <>
      <SEO
        title="AI简历生成器 - 免费在线智能简历制作工具 | ndtool"
        description="免费AI简历生成器，一键生成专业简历。200+精美模板，AI智能优化，支持PDF/Word导出。应届生、职场转型首选在线简历工具。"
      />
      <div className="landing-page">
        <Navbar />
        <HeroSection />
        <StatsSection />
        <FeaturesSection />
        <HowItWorksSection />
        <TestimonialsSection />
        <PricingSection />
        <DownloadSection />
        <FAQSection />
        <CTASection />
        <Footer />
      </div>
    </>
  );
}
