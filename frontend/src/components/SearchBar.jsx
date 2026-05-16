import { useState } from "react";
import { Search, X } from "lucide-react";

export function SearchBar({ value, onChange, onReset }) {
  const [input, setInput] = useState(value || "");

  const handleSubmit = (e) => {
    e.preventDefault();
    onChange(input);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full">
      <div className="relative flex-1">
        <Search
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
          size={18}
        />
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Buscar artigos..."
          className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg
                     focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        {input && (
          <button
            type="button"
            onClick={() => { setInput(""); onChange(""); }}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400
                       hover:text-gray-600"
          >
            <X size={16} />
          </button>
        )}
      </div>
      <button
        type="submit"
        className="px-5 py-2 bg-primary-600 text-white rounded-lg
                   hover:bg-primary-700 transition-colors"
      >
        Buscar
      </button>
      <button
        type="button"
        onClick={onReset}
        className="px-4 py-2 border border-gray-300 rounded-lg
                   hover:bg-gray-100 transition-colors text-sm"
      >
        Limpar
      </button>
    </form>
  );
}
