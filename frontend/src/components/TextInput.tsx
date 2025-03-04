function TextInput({ value, onChange, placeholder }: { value: string, onChange: (e: React.ChangeEvent<HTMLInputElement>) => void, placeholder: string }) {
  return (
    <input type="text" 
    className="rounded-lg w-full px-6 py-3 border border-gray-300 hover:border-purple-400 transition-colors focus:outline-none focus:ring-3 focus:ring-purple-200 focus:border-purple-400" 
    value={value} onChange={onChange} placeholder={placeholder} />
  )
}

export default TextInput