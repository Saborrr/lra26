import { useEffect, useRef } from 'react';

type Star = {
  x: number;
  y: number;
  depth: number;
  radius: number;
  alpha: number;
  phase: number;
  twinkle: number;
  driftX: number;
  driftY: number;
  color: string;
};

const STAR_COLORS = ['220,235,255', '255,255,255', '178,215,255', '214,198,255'] as const;

export function CosmicBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');
    if (!canvas || !context) return undefined;

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let width = 0;
    let height = 0;
    let stars: Star[] = [];
    let frame = 0;
    let lastTime = 0;

    const createStars = () => {
      const count = Math.min(360, Math.max(130, Math.round((width * height) / 6200)));
      stars = Array.from({ length: count }, () => {
        const depth = Math.random();
        return {
          x: Math.random() * width,
          y: Math.random() * height,
          depth,
          radius: 0.35 + depth * depth * 1.55,
          alpha: 0.2 + depth * 0.66,
          phase: Math.random() * Math.PI * 2,
          twinkle: 0.00035 + Math.random() * 0.00075,
          driftX: 0.45 + depth * 1.1,
          driftY: 0.16 + depth * 0.48,
          color: STAR_COLORS[Math.floor(Math.random() * STAR_COLORS.length)] ?? STAR_COLORS[0],
        };
      });
    };

    const resize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      createStars();
    };

    const render = (time: number) => {
      const elapsed = Math.min(32, time - lastTime || 16.7);
      lastTime = time;
      context.clearRect(0, 0, width, height);

      for (const star of stars) {
        if (!reducedMotion) {
          star.x += star.driftX * elapsed * 0.001;
          star.y += star.driftY * elapsed * 0.001;
          if (star.x > width + 4) star.x = -4;
          if (star.y > height + 4) star.y = -4;
        }
        const pulse = reducedMotion ? 1 : 0.76 + Math.sin(time * star.twinkle + star.phase) * 0.24;
        context.beginPath();
        context.fillStyle = `rgba(${star.color},${star.alpha * pulse})`;
        context.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        context.fill();
      }

      context.save();
      context.globalCompositeOperation = 'screen';
      for (const star of stars) {
        if (star.depth < 0.84) continue;
        const glow = context.createRadialGradient(
          star.x,
          star.y,
          0,
          star.x,
          star.y,
          star.radius * 5,
        );
        glow.addColorStop(0, `rgba(${star.color},${star.alpha * 0.32})`);
        glow.addColorStop(1, `rgba(${star.color},0)`);
        context.fillStyle = glow;
        context.fillRect(
          star.x - star.radius * 5,
          star.y - star.radius * 5,
          star.radius * 10,
          star.radius * 10,
        );
      }
      context.restore();

      if (!reducedMotion) frame = window.requestAnimationFrame(render);
    };

    resize();
    render(0);
    window.addEventListener('resize', resize, { passive: true });
    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return (
    <div className="cosmos" aria-hidden="true">
      <canvas ref={canvasRef} className="star-canvas" />
      <div className="nebula nebula-one" />
      <div className="nebula nebula-two" />
      <div className="orbit"><span /></div>
      <div className="cosmic-vignette" />
    </div>
  );
}
