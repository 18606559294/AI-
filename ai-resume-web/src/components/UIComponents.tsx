import { ReactNode } from 'react';

// ============================================
// Button Components - Futuristic Tech Style
// ============================================

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'accent' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: ReactNode;
  children: ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  children,
  className = '',
  disabled,
  ...props
}: ButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center gap-2 font-semibold rounded-xl transition-all duration-300 cursor-pointer';

  const variantClasses = {
    primary: 'btn-primary text-white',
    secondary: 'btn-secondary',
    ghost: 'btn-ghost',
    accent: 'btn-accent',
    danger: 'px-6 py-3 rounded-xl font-semibold bg-gradient-to-r from-rose-500 to-red-600 text-white hover:scale-105 shadow-lg shadow-rose-500/30',
  };

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3',
    lg: 'px-8 py-4 text-lg',
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <div className="spinner w-5 h-5 border-2 border-current border-t-transparent rounded-full" />
      ) : icon}
      {children}
    </button>
  );
}

// ============================================
// Card Components
// ============================================

interface CardProps {
  variant?: 'glass' | 'neon' | 'hover' | 'solid';
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}

export function Card({ variant = 'solid', children, className = '', onClick }: CardProps) {
  const variantClasses = {
    glass: 'card-glass',
    neon: 'card-neon',
    hover: 'card-hover cursor-pointer',
    solid: 'rounded-2xl p-6 bg-slate-800/50 border border-slate-700/50',
  };

  return (
    <div className={`${variantClasses[variant]} ${onClick ? 'cursor-pointer' : ''} ${className}`} onClick={onClick}>
      {children}
    </div>
  );
}

// ============================================
// Input Components
// ============================================

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: ReactNode;
}

export function Input({ label, error, icon, className = '', ...props }: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-slate-300 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {icon && (
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
            {icon}
          </div>
        )}
        <input
          className={`input-cyber ${icon ? 'pl-12' : ''} ${error ? 'border-rose-500' : ''} ${className}`}
          {...props}
        />
      </div>
      {error && (
        <p className="mt-2 text-sm text-rose-400">{error}</p>
      )}
    </div>
  );
}

// ============================================
// Badge Components
// ============================================

interface BadgeProps {
  variant?: 'neon' | 'outline' | 'success' | 'warning' | 'error';
  children: ReactNode;
}

export function Badge({ variant = 'neon', children }: BadgeProps) {
  const variantClasses = {
    neon: 'badge-neon text-white',
    outline: 'badge-outline',
    success: 'px-3 py-1 rounded-full text-xs font-semibold bg-green-500/20 text-green-400 border border-green-500/50',
    warning: 'px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/50',
    error: 'px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/50',
  };

  return <span className={variantClasses[variant]}>{children}</span>;
}

// ============================================
// Gradient Text Component
// ============================================

interface GradientTextProps {
  children: ReactNode;
  variant?: 'primary' | 'accent' | 'full';
  className?: string;
}

export function GradientText({ children, variant = 'full', className = '' }: GradientTextProps) {
  const variantClasses = {
    primary: 'text-gradient-primary',
    accent: 'text-gradient-accent',
    full: 'text-gradient',
  };

  return <span className={`${variantClasses[variant]} ${className}`}>{children}</span>;
}

// ============================================
// Loading Spinner Component
// ============================================

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
}

export function Spinner({ size = 'md' }: SpinnerProps) {
  const sizeClasses = {
    sm: 'w-5 h-5',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return <div className={`spinner ${sizeClasses[size]} border-4 border-slate-700 border-t-sky-500 rounded-full`} />;
}

// ============================================
// Divider Component
// ============================================

export function Divider({ className = '' }: { className?: string }) {
  return <div className={`divider-gradient my-6 ${className}`} />;
}

// ============================================
// Glass Container Component
// ============================================

interface GlassContainerProps {
  children: ReactNode;
  className?: string;
}

export function GlassContainer({ children, className = '' }: GlassContainerProps) {
  return (
    <div className={`card-glass ${className}`}>
      {children}
    </div>
  );
}

// ============================================
// Neon Border Container
// ============================================

interface NeonContainerProps {
  children: ReactNode;
  color?: 'blue' | 'purple' | 'pink' | 'green';
  className?: string;
}

export function NeonContainer({ children, color = 'blue', className = '' }: NeonContainerProps) {
  const colorClasses = {
    blue: 'shadow-neon-blue',
    purple: 'shadow-neon-purple',
    pink: 'shadow-neon-pink',
    green: 'shadow-green-500/50',
  };

  return (
    <div className={`rounded-2xl p-6 bg-slate-900/50 border ${colorClasses[color]} ${className}`}>
      {children}
    </div>
  );
}

// ============================================
// Orb Background Component
// ============================================

interface OrbProps {
  color?: 'primary' | 'accent';
  size?: number;
  className?: string;
}

export function Orb({ color = 'primary', size = 400, className = '' }: OrbProps) {
  const colorClasses = {
    primary: 'orb-primary',
    accent: 'orb-accent',
  };

  return (
    <div
      className={`bg-orb ${colorClasses[color]} ${className}`}
      style={{ width: size, height: size }}
    />
  );
}

// ============================================
// Section Component
// ============================================

interface SectionProps {
  children: ReactNode;
  className?: string;
  container?: boolean;
}

export function Section({ children, className = '', container = true }: SectionProps) {
  return (
    <section className={`py-20 ${className}`}>
      {container ? (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {children}
        </div>
      ) : children}
    </section>
  );
}

// ============================================
// Icon Wrapper Component
// ============================================

interface IconWrapperProps {
  children: ReactNode;
  variant?: 'primary' | 'accent' | 'glass';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function IconWrapper({ children, variant = 'glass', size = 'md', className = '' }: IconWrapperProps) {
  const sizeClasses = {
    sm: 'w-10 h-10',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
  };

  const variantClasses = {
    primary: 'bg-primary-500/20 text-primary-400',
    accent: 'bg-accent-500/20 text-accent-400',
    glass: 'glass-effect text-slate-300',
  };

  return (
    <div className={`${sizeClasses[size]} ${variantClasses[variant]} rounded-xl flex items-center justify-center ${className}`}>
      {children}
    </div>
  );
}

// ============================================
// Status Indicator Component
// ============================================

interface StatusIndicatorProps {
  status: 'online' | 'offline' | 'away' | 'busy';
  showText?: boolean;
}

export function StatusIndicator({ status, showText = false }: StatusIndicatorProps) {
  const statusConfig = {
    online: { color: 'bg-green-500', text: '在线' },
    offline: { color: 'bg-slate-500', text: '离线' },
    away: { color: 'bg-amber-500', text: '离开' },
    busy: { color: 'bg-rose-500', text: '忙碌' },
  };

  const config = statusConfig[status];

  return (
    <div className="flex items-center gap-2">
      <span className={`relative flex h-3 w-3`}>
        <span className={`absolute inline-flex h-full w-full rounded-full ${config.color} opacity-75 animate-ping`}></span>
        <span className={`relative inline-flex rounded-full h-3 w-3 ${config.color}`}></span>
      </span>
      {showText && <span className="text-sm text-slate-400">{config.text}</span>}
    </div>
  );
}
