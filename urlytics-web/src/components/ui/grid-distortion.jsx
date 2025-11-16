"use client";
import React from "react";

export default function GridDistortion({
  className = "",
  gridSize = 50,
  color = "rgba(255, 255, 255, 0.1)",
  children,
}) {
  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 dark:from-slate-900 dark:via-purple-900 dark:to-slate-900" />
      
      {/* Animated grid */}
      <div className="absolute inset-0 grid-distortion-effect">
        <svg
          className="absolute inset-0 h-full w-full"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <pattern
              id="grid"
              width={gridSize}
              height={gridSize}
              patternUnits="userSpaceOnUse"
            >
              <path
                d={`M ${gridSize} 0 L 0 0 0 ${gridSize}`}
                fill="none"
                stroke={color}
                strokeWidth="1"
              />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
          
          {/* Animated distortion overlay */}
          <rect 
            width="100%" 
            height="100%" 
            fill="url(#grid)" 
            className="animate-grid-distortion"
            style={{
              transformOrigin: 'center',
              animation: 'gridDistortion 20s ease-in-out infinite'
            }}
          />
        </svg>
      </div>

      {/* Radial gradient overlay */}
      <div className="absolute inset-0 bg-gradient-radial from-transparent via-transparent to-black/30" />

      {/* Content */}
      <div className="relative z-10">
        {children}
      </div>

      <style jsx>{`
        @keyframes gridDistortion {
          0%, 100% {
            transform: rotate(0deg) scale(1) skew(0deg);
          }
          25% {
            transform: rotate(2deg) scale(1.05) skew(1deg);
          }
          50% {
            transform: rotate(-1.5deg) scale(1.02) skew(-0.5deg);
          }
          75% {
            transform: rotate(3deg) scale(1.08) skew(1.5deg);
          }
        }

        .animate-grid-distortion {
          animation: gridDistortion 20s ease-in-out infinite;
        }

        .bg-gradient-radial {
          background: radial-gradient(circle at center, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
        }
      `}</style>
    </div>
  );
}
