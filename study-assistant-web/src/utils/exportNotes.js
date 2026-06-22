export function exportNotes(messages, topic) {
  const headerLines = [
    "# AI Study Assistant Notes",
    "",
    "## Topic",
    topic || "",
    "",
    "## Conversation",
    "",
  ];

  const bodyLines = messages.flatMap((msg) => {
    const roleLabel = msg.role === "user" ? "User" : msg.role === "assistant" ? "Assistant" : msg.role;
    return [
      `### ${roleLabel}`,
      msg.content || "",
      "",
    ];
  });

  const markdown = [...headerLines, ...bodyLines].join("\n");
  const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
  return { blob, filename: "study-notes.md" };
}
