interface ButtonProps {
  text: string;
  onClick?: () => void;
  type: "submit" | "button";
}

export const Button = ({ text, onClick, type }: ButtonProps) => {
  return (
    <button type={type} className="flex items-center gap-2 focus:ring-3 focus:ring-purple-200 active:ring-purple-200 active:ring-3 transition-colors rounded-lg group/btn cursor-pointer text-white gradient-button btn-purple px-6 py-3" onClick={onClick}>
      <span>{text}</span>
      <div className="flex items-center opacity-50 group-hover/btn:opacity-100 transition-opacity">
        <svg role="img" viewBox="0 0 16 16" width="10" height="10" fill="currentColor" className="size-[0.7em]">
          <path d="M7.293 1.707L13.586 8l-6.293 6.293a1 1 0 001.414 1.414l7-7a.999.999 0 000-1.414l-7-7a1 1 0 00-1.414 1.414z"></path>
        </svg>
      </div>
    </button>
  )
}
