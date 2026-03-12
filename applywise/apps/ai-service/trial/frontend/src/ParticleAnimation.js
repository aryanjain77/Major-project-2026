import React, { useEffect, useRef } from 'react';

class Particle {
  constructor(x = 0, y = 0) {
    this.reset();
    this.fadingSpeed = Math.random();
  }

  update() {
    this.position.x += Math.random() * 2 - 1;
    this.position.y -= this.velocity.y;
    this.alpha -= this.fadingSpeed;

    if (this.alpha < 0) {
      this.reset();
    }
  }

  reset() {
    this.position = { x: 0, y: 0 };
    this.velocity = { x: 0, y: Math.random() - 0.4 };
    this.alpha = 1;
    this.fadingSpeed = Math.random() * 0.03 + 0.005;
  }
}

class ParticleEmitter {
  constructor(x = 0, y = 0) {
    this.position = { x, y };
    this.particles = [];
    this.particlesNumber = 6;

    for (let i = 0; i < this.particlesNumber; i++) {
      const particle = new Particle();
      this.particles.push(particle);
    }
  }

  update() {
    for (let particle of this.particles) {
      particle.update();
    }
  }
}

const ParticleAnimation = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');
    const fps = 120;
    const fpsInterval = 1000 / fps;
    let then = Date.now();
    let raf;

    const particleEmitters = [];
    const radius = 200;

    for (let i = 0; i < 360; i++) {
      const particleEmitter = new ParticleEmitter(0, radius);
      particleEmitters.push(particleEmitter);
    }

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const render = () => {
      for (let particleEmitter of particleEmitters) {
        particleEmitter.update();
        context.save();
        context.translate(canvas.width / 2, canvas.height / 2);
        context.rotate((particleEmitters.indexOf(particleEmitter) * Math.PI) / 180);
        for (let particle of particleEmitter.particles) {
          particle.update();
          context.globalAlpha = particle.alpha;
          context.beginPath();
          context.arc(particle.position.x, particleEmitter.position.y - particle.position.y, 1, 0, Math.PI * 2);
          context.fillStyle = '#ecf0f1';
          context.fill();
          context.closePath();
        }
        context.restore();
      }
    };

    const loop = () => {
      raf = window.requestAnimationFrame(loop);
      const now = Date.now();
      const delta = now - then;

      if (delta > fpsInterval) {
        context.clearRect(0, 0, canvas.width, canvas.height);
        render();
        then = now;
      }
    };

    const handleResize = () => {
      resize();
      window.cancelAnimationFrame(raf);
      context.clearRect(0, 0, canvas.width, canvas.height);
      loop();
    };

    resize();
    window.addEventListener('resize', handleResize);
    loop();

    return () => {
      window.cancelAnimationFrame(raf);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return <canvas id="canvas" className="canvas" ref={canvasRef} />;
};

export default ParticleAnimation;