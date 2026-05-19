import { useState, useRef, useEffect } from 'react';
import { BiSearch } from 'react-icons/bi';

export default function SearchBar({ value, onChange }) {
    const [input, setInput] = useState(value || '');
    const timer = useRef(null);

    useEffect(() => {
        setInput(value);
    }, [value]);

    const handleChange = (e) => {
        setInput(e.target.value);
        clearTimeout(timer.current);
        timer.current = setTimeout(() => {
            onChange(e.target.value);
        }, 300);
    };

    return (
        <div className="relative w-full max-w-lg mx-auto">
            <BiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-earth text-xl" />
            <input
                type="text"
                value={input}
                onChange={handleChange}
                placeholder="Search recipes..."
                className="w-full pl-12 pr-4 py-3 rounded-full bg-white/80 backdrop-blur-sm shadow-md border border-earth/20 focus:outline-none focus:ring-2 focus:ring-terracotta text-dark-brown placeholder:text-earth/70"
            />
        </div>
    );
}