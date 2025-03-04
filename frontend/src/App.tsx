import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from 'react-markdown';
import CustomSVG from "./main";
import { Button } from "./components/Button";
import TextInput from "./components/TextInput";
import Loader from "./components/Loader";

type Message = {
  content: string;
  isUser: boolean;
  role?: 'user' | 'assistant';
};

const placeholderMD = `# Hello!
                      
                      This is some sample markdown with:

                      - A bullet point
                      - Another point
                      - And a third

                      ## Code Example
                      \`\`\`js
                      const greeting = "Hello World!";
                      console.log(greeting);
                      \`\`\`

                      *Italics* and **bold** text are supported too.`

const botMessage: Message = { content: placeholderMD, isUser: false };


function App() {
  const [input, setInput] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const askQuestion = async (text: string, messageHistory: Message[]): Promise<string> => {
    setLoading(true);
    const formattedHistory = messageHistory.map(msg => ({
      role: msg.isUser ? 'user' : 'assistant',
      content: msg.content
    }));

    const res = await fetch("http://localhost:8000/api/embed", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        text,
        history: formattedHistory
      }),
    });
    const data = await res.json();
    setLoading(false);
    console.log(data);
    return data.answer.content[0].text;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = { content: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput("");

    const response = await askQuestion(input, [...messages, userMessage]);
    const botMessage: Message = { content: response, isUser: false };
    setMessages(prev => [...prev, botMessage]);
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-gray-100 overflow-hidden">
      {/* Background SVG Wrapper */}
      <div className="fixed top-0 left-0 w-full h-auto pointer-events-none">
        <CustomSVG />
      </div>

      <div className="flex flex-col max-w-2xl w-full z-10">
        <header>
          <h1 className="text-4xl text-center text-slate-800 my-6">Got questions?</h1>
          <p className="text-center text-slate-600">Search the Fly.io docs using natural language. Ask away!</p>
        </header>
        {/* Main content container */}
        <div className="relative bg-white rounded-lg shadow-lg p-8  my-8">
        {/* Chat messages */}
        <div className="flex-1 overflow-auto">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`mb-4 ${
                message.isUser ? "text-right" : "text-left"
              }`}
            >
              <div
                className={`inline-block p-4 rounded-lg ${
                  message.isUser
                    ? "bg-purple-700 text-white"
                    : "bg-gray-100 text-black"
                }`}
              >
                {message.isUser ? (
                  message.content
                ) : (
                  <div className="markdown-content">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && 
          <div className="flex mb-8">
            <Loader />
          </div>
          }
          <div ref={messagesEndRef} />
        </div>

        {/* Input form */}
        <form onSubmit={handleSubmit} className="flex gap-2">
          <TextInput value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type a message..."/>
          <Button text="Send" type="submit" />
        </form>
        </div>
      </div>
      {/* Background Image */}
      <img 
        src="/cloud-city.png"
        alt="Cloud City"
        className="fixed bottom-0 left-1/2 -translate-x-1/2 w-screen h-auto pointer-events-none"
      />
    </div>
  );
}

export default App;
