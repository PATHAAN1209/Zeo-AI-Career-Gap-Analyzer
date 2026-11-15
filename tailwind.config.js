/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        hud: {
          bg: "#050B14",
          panel: "#0B1626",
          panelHover: "#0E1C30",
          border: "#1E3A5F",
          borderBright: "#00E5FF",
          cyan: "#00E5FF",
          electric: "#2979FF",
          text: "#E6F6FF",
          muted: "#7FA0BF",
          have: "#00F5A0",
          partial: "#FFC400",
          missing: "#FF4D4D",
          dimCyan: "rgba(0, 229, 255, 0.12)",
          glowCyan: "rgba(0, 229, 255, 0.35)",
        }
      },
      fontFamily: {
        orbitron: ['Orbitron', 'sans-serif'],
        inter: ['Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      backgroundImage: {
        'hud-gradient': 'linear-gradient(135deg, #00E5FF, #2979FF)',
        'hud-radial': 'radial-gradient(circle at 50% 0%, rgba(0, 229, 255, 0.15) 0%, rgba(5, 11, 20, 0) 70%)',
        'grid-pattern': 'radial-gradient(circle, rgba(0, 229, 255, 0.12) 1px, transparent 1px)',
      },
      boxShadow: {
        'hud-cyan': '0 0 20px rgba(0, 229, 255, 0.25)',
        'hud-cyan-lg': '0 0 35px rgba(0, 229, 255, 0.45)',
        'hud-panel': '0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 0 0 1px rgba(30, 58, 95, 0.6)',
        'reactor-glow': '0 0 50px rgba(0, 229, 255, 0.4), inset 0 0 30px rgba(41, 121, 255, 0.3)',
      },
      animation: {
        'pulse-glow': 'pulseGlow 2.5s ease-in-out infinite',
        'scanner-sweep': 'scannerSweep 2.2s ease-in-out infinite alternate',
        'radar-spin': 'radarSpin 10s linear infinite',
        'laser-bar': 'laserBar 1.8s ease-in-out infinite',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { opacity: '0.4', transform: 'scale(0.98)' },
          '50%': { opacity: '0.9', transform: 'scale(1.03)' },
        },
        scannerSweep: {
          '0%': { top: '0%' },
          '100%': { top: '100%' },
        },
        radarSpin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        laserBar: {
          '0%': { transform: 'translateY(-100%)', opacity: '0.3' },
          '50%': { opacity: '1' },
          '100%': { transform: 'translateY(100%)', opacity: '0.3' },
        }
      }
    },
  },
  plugins: [],
}
