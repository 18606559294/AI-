import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <>
      <nav className={`lp-navbar${scrolled ? ' scrolled' : ''}`}>
        <div className="lp-navbar-inner">
          <Link to="/" className="lp-logo">
            <span className="lp-logo-icon">N</span>
            ndtool
          </Link>

          <div className="lp-nav-menu">
            <Link to="/login" className="lp-nav-link">AI 简历</Link>
            <Link to="/templates" className="lp-nav-link">模板</Link>
            <Link to="/about" className="lp-nav-link">关于</Link>
            <a href="/resources/" className="lp-nav-link">资源工具</a>
            <Link to="/login" className="lp-nav-link lp-nav-login">登录</Link>
            <Link to="/register" className="lp-nav-cta">免费注册</Link>
          </div>

          <button
            className={`lp-hamburger${menuOpen ? ' open' : ''}`}
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="菜单"
          >
            <span /><span /><span />
          </button>
        </div>
      </nav>

      <div className={`lp-mobile-menu${menuOpen ? ' open' : ''}`}>
        <Link to="/login" className="lp-nav-link" onClick={() => setMenuOpen(false)}>AI 简历</Link>
        <Link to="/templates" className="lp-nav-link" onClick={() => setMenuOpen(false)}>模板</Link>
        <Link to="/about" className="lp-nav-link" onClick={() => setMenuOpen(false)}>关于</Link>
        <a href="/resources/" className="lp-nav-link">资源工具</a>
        <Link to="/login" className="lp-nav-link" onClick={() => setMenuOpen(false)}>登录</Link>
        <Link to="/register" className="lp-nav-cta" onClick={() => setMenuOpen(false)}>免费注册</Link>
      </div>
    </>
  );
}
