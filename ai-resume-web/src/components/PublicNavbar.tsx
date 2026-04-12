import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const NAV_ITEMS = [
  { path: '/', label: '首页' },
  { path: '/career', label: '职业智能' },
  { path: '/about', label: '关于' },
  { path: '/help', label: '帮助' },
  { path: '/trae', label: 'Trae AI' },
  { path: '/terms', label: '条款' },
  { path: '/privacy', label: '隐私' },
] as const;

export default function PublicNavbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  return (
    <>
      <nav className={`pub-nav${scrolled ? ' scrolled' : ''}`}>
        <div className="pub-nav-inner">
          <Link to="/" className="pub-nav-logo">
            <span className="pub-nav-logo-icon">N</span>
            ndtool
          </Link>

          <div className="pub-nav-links">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`pub-nav-link${location.pathname === item.path ? ' active' : ''}`}
              >
                {item.label}
              </Link>
            ))}
          </div>

          <div className="pub-nav-actions">
            <Link to="/login" className="pub-nav-login">登录</Link>
            <Link to="/register" className="pub-nav-cta">免费注册</Link>
          </div>

          <button
            className={`pub-hamburger${menuOpen ? ' open' : ''}`}
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="菜单"
          >
            <span /><span /><span />
          </button>
        </div>
      </nav>

      <div className={`pub-mobile-menu${menuOpen ? ' open' : ''}`}>
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`pub-nav-link${location.pathname === item.path ? ' active' : ''}`}
            onClick={() => setMenuOpen(false)}
          >
            {item.label}
          </Link>
        ))}
        <Link to="/login" className="pub-nav-link" onClick={() => setMenuOpen(false)}>登录</Link>
        <Link to="/register" className="pub-nav-cta" onClick={() => setMenuOpen(false)}>免费注册</Link>
      </div>
    </>
  );
}
