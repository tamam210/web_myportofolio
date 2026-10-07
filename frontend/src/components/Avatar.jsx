export default function Avatar() {
  return (
    <svg
      className="avatar-svg"
      viewBox="0 0 200 200"
      role="img"
      aria-label="Animasi avatar Tamam"
    >
      <defs>
        <linearGradient id="avatarHoodie" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#7c3aed" />
          <stop offset="100%" stopColor="#a855f7" />
        </linearGradient>
        <radialGradient id="avatarBg" cx="50%" cy="40%" r="70%">
          <stop offset="0%" stopColor="#3b0f63" />
          <stop offset="100%" stopColor="#160d26" />
        </radialGradient>
      </defs>

      <circle cx="100" cy="100" r="96" fill="url(#avatarBg)" />

      <g className="avatar-char">
        <circle cx="100" cy="76" r="44" fill="#2b1b46" />
        <circle cx="62" cy="86" r="9" fill="#ffcfa8" />
        <circle cx="138" cy="86" r="9" fill="#ffcfa8" />
        <rect x="90" y="106" width="20" height="30" rx="10" fill="#f0b98d" />
        <circle cx="100" cy="80" r="40" fill="#ffcfa8" />

        <circle cx="78" cy="62" r="15" fill="#2b1b46" />
        <circle cx="100" cy="55" r="17" fill="#2b1b46" />
        <circle cx="122" cy="62" r="15" fill="#2b1b46" />

        <g className="avatar-eyes">
          <ellipse cx="86" cy="88" rx="6" ry="8" fill="#2b1b46" />
          <ellipse cx="114" cy="88" rx="6" ry="8" fill="#2b1b46" />
          <circle cx="88" cy="85" r="2" fill="#fff" />
          <circle cx="116" cy="85" r="2" fill="#fff" />
        </g>

        <path
          d="M96 97 Q100 101 104 97"
          fill="none"
          stroke="#e0a878"
          strokeWidth="3"
          strokeLinecap="round"
        />
        <path
          d="M90 105 Q100 116 110 105"
          fill="none"
          stroke="#4a2c1a"
          strokeWidth="4"
          strokeLinecap="round"
        />
        <circle cx="75" cy="100" r="6" fill="#f19bb0" opacity="0.55" />
        <circle cx="125" cy="100" r="6" fill="#f19bb0" opacity="0.55" />

        <path
          d="M46 200 V170 C46 144 68 130 100 130 C132 130 154 144 154 170 V200 Z"
          fill="url(#avatarHoodie)"
        />
        <path
          d="M86 131 Q100 147 114 131"
          fill="none"
          stroke="#5b21b6"
          strokeWidth="5"
          strokeLinecap="round"
        />
        <path
          d="M100 148 V200"
          stroke="#5b21b6"
          strokeWidth="4"
          opacity="0.6"
        />

        <path
          d="M56 154 L50 190"
          stroke="#7c3aed"
          strokeWidth="20"
          strokeLinecap="round"
        />
        <circle cx="49" cy="194" r="10" fill="#ffcfa8" />

        <g className="avatar-arm">
          <path
            d="M144 150 L170 112"
            stroke="#8b5cf6"
            strokeWidth="20"
            strokeLinecap="round"
          />
          <circle cx="174" cy="104" r="11" fill="#ffcfa8" />
        </g>
      </g>
    </svg>
  );
}
