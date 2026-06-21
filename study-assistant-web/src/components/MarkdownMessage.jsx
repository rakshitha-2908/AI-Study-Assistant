import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { FiCheck, FiCopy } from "react-icons/fi";

function CodeBlock({ className, children }) {
  const [copied, setCopied] = useState(false);
  const language = (className || "").replace("language-", "") || "text";
  const code = String(children).replace(/\n$/, "");

  function handleCopy() {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <div className="relative my-3 rounded-lg overflow-hidden border border-gray-800/40">
      <div className="flex items-center justify-between bg-[#1f1f1f] px-3.5 py-1.5">
        <span className="text-[11px] text-gray-400 font-mono">{language}</span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-[11px] text-gray-400 hover:text-gray-200 transition-colors"
        >
          {copied ? <FiCheck size={12} /> : <FiCopy size={12} />}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{ margin: 0, padding: "12px 14px", fontSize: "13px", background: "#181818" }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

/**
 * Renders assistant message content as real markdown — headers, bullet
 * lists, bold text, tables, and fenced code blocks all render properly
 * instead of showing literal "#" and backtick characters.
 */
function MarkdownMessage({ content }) {
  return (
    <div className="prose prose-sm max-w-none prose-headings:font-semibold prose-headings:text-gray-900 prose-h3:text-[15px] prose-h3:mt-3 prose-h3:mb-1.5 prose-p:my-1.5 prose-p:leading-relaxed prose-ul:my-1.5 prose-li:my-0.5 prose-strong:text-gray-900 prose-table:text-sm">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code({ className, children, ...props }) {
            const isInline = !className;
            if (isInline) {
              return (
                <code className="bg-gray-200/70 text-gray-800 rounded px-1.5 py-0.5 text-[13px]" {...props}>
                  {children}
                </code>
              );
            }
            return <CodeBlock className={className}>{children}</CodeBlock>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}


export default MarkdownMessage;