import { clsx } from 'clsx';
import { ReactNode } from 'react';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  padding?: string;
}

export function GlassCard({ 
  children, 
  className = '', 
  padding = 'p-8' 
}: GlassCardProps) {
  return (
    <div className={clsx(
      'glass-card',
      padding,
      className
    )}>
      {children}
    </div>
  );
}