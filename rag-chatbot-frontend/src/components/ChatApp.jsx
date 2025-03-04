import React, { useState } from "react";
import axios from "axios";

const ChatApp = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add the user's message to the chat
    setMessages((prev) => [...prev, { text: input, sender: "user" }]);

    try {
      // Send the question to the backend
      const response = await axios.post("http://localhost:8000/generate/", {
        question: input,
      });

       console.log("Backend Response:", response.data.response);

      // Add the AI's response to the chat
      setMessages((prev) => [
        ...prev,
        { text: response.data.response, sender: "ai" },
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages((prev) => [
        ...prev,
        { text: "Failed to get a response from the server.", sender: "ai" },
      ]);
    }

    // Clear the input field
    setInput("");
  };

  return (
    <div style={styles.container}>
       
      <div style={styles.navbar}>Chatbot</div>

      <div style={styles.sidebar}>
        <h3 style={styles.sidebarTitle}>Suggested Questions</h3>
        <ul style={styles.questionList}>
          <li onClick={() => setInput("What are the visiting hours at the hospital?")}>What are the visiting hours at the hospital?</li>
          <li onClick={() => setInput("Who are the cardiology specialists at Harmony Health Center?")}>Who are the cardiology specialists at Harmony Health Center?</li>
          <li onClick={() => setInput("What payment options are available at the hospital?")}>What payment options are available at the hospital?</li>
          <li onClick={() => setInput("What are the patient reviews for Dr. Laura Grant?")}>What are the patient reviews for Dr. Laura Grant?</li>
          <li onClick={() => setInput("What facilities does Harmony Health Center offer?")}>What facilities does Harmony Health Center offer?</li>
          <li onClick={() => setInput("What pediatric services are available at the hospital?")}>What pediatric services are available at the hospital?</li>

        </ul>
      </div>
      <div style={styles.chatSection}>
        <div style={styles.chatContainer}>
          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                ...styles.message,
                textAlign: msg.sender === "user" ? "right" : "left",
                backgroundColor: msg.sender === "user" ? "#007bff" : "#f1f1f1",
                color: msg.sender === "user" ? "#fff" : "#000",
              }}
            >
              {msg.text}
            </div>
          ))}
        </div>
        <div style={styles.inputContainer}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            style={styles.input}
            placeholder="Type your question..."
          />
          <button onClick={handleSend} style={styles.button}>
            Send
          </button>
        </div>
    </div>
    </div>
  );
};

// const styles = {
//   container: {
//     display: "flex",
//     height: "100vh",
//     backgroundColor: "#f9f9f9",
//   },
//   navbar: {
//     position: "fixed",
//     top: 0,
//     left: 0,
//     right: 0,
//     height: "60px",
//     backgroundColor: "#fff",
//     color: "#333",
//     display: "flex",
//     alignItems: "center",
//     paddingLeft: "20px",
//     fontSize: "18px",
//     fontWeight: "bold",
//     boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
//     zIndex: 1000,
//   },
//   sidebar: {
//     position: "fixed",
//     top: "60px",
//     left: 0,
//     width: "260px",
//     height: "calc(100vh - 60px)",
//     backgroundColor: "#f4f4f4",
//     padding: "20px",
//     overflowY: "auto",
//     boxShadow: "2px 0 4px rgba(0, 0, 0, 0.1)",
//   },
//   chatSection: {
//     flex: 1,
//     marginLeft: "260px",
//     display: "flex",
//     flexDirection: "column",
//     alignItems: "center",
//     justifyContent: "center",
//     paddingTop: "80px",
//   },
//   chatContainer: {
//     width: "85%",
//     height: "70vh", // Fixed height to prevent resizing
//     display: "flex",
//     flexDirection: "column",
//     justifyContent: "flex-start", // Align messages to the top
//     alignItems: "center",
//     padding: "20px",
//     borderRadius: "10px",
//     backgroundColor: "#fff",
//     border: "1px solid #ddd",
//     boxShadow: "0 2px 6px rgba(0, 0, 0, 0.1)",
//     overflowY: "auto", // Scroll if messages exceed the container height
//   },
//   messageContainer: {
//     display: "flex",
//     flexDirection: "column",
//     width: "100%",
//     overflowY: "auto",
//     flex: 1, // Allows messages to expand while keeping the chat container fixed
//   },
//   message: {
//     padding: "12px",
//     borderRadius: "8px",
//     marginBottom: "10px",
//     maxWidth: "70%",
//     wordWrap: "break-word",
//   },
//   aiMessage: {
//     alignSelf: "flex-start",
//     backgroundColor: "#e3f2fd",
//     color: "#000",
//   },
//   userMessage: {
//     alignSelf: "flex-end",
//     backgroundColor: "#000",
//     color: "#fff",
//   },
//   inputContainer: {
//     display: "flex",
//     alignItems: "center",
//     backgroundColor: "#fff",
//     borderRadius: "30px",
//     padding: "10px",
//     boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
//     width: "65%",
//     marginTop: "10px",
//     border: "1px solid #ccc",
//   },
//   input: {
//     flex: 1,
//     padding: "12px",
//     border: "none",
//     outline: "none",
//     fontSize: "16px",
//   },
//   sendButton: {
//     backgroundColor: "#000",
//     color: "#fff",
//     border: "none",
//     padding: "12px",
//     borderRadius: "50%",
//     cursor: "pointer",
//     display: "flex",
//     alignItems: "center",
//     justifyContent: "center",
//     transition: "background 0.2s ease-in-out",
//   },
// };
const styles = {
  container: {
    display: "flex",
    height: "100vh",
    backgroundColor: "#f9f9f9",
  },
  navbar: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    height: "60px",
    backgroundColor: "#fff",
    color: "#333",
    display: "flex",
    alignItems: "center",
    paddingLeft: "20px",
    fontSize: "18px",
    fontWeight: "bold",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    zIndex: 1000,
  },
  sidebar: {
    position: "fixed",
    top: "60px",
    left: 0,
    width: "260px",
    height: "calc(100vh - 60px)",
    backgroundColor: "#f4f4f4",
    padding: "20px",
    overflowY: "auto",
    boxShadow: "2px 0 4px rgba(0, 0, 0, 0.1)",
    zIndex: 999,
  },
  chatSection: {
    flex: 1,
    marginLeft: "260px",
    marginTop: "60px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "20px",
  },
  chatContainer: {
    width: "85%",
    height: "calc(100vh - 200px)",
    display: "flex",
    flexDirection: "column",
    borderRadius: "10px",
    backgroundColor: "#fff",
    border: "1px solid #ddd",
    boxShadow: "0 2px 6px rgba(0, 0, 0, 0.1)",
  },
  messageContainer: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    padding: "20px",
    overflowY: "auto",
  },
  message: {
    padding: "12px",
    borderRadius: "8px",
    maxWidth: "70%",
    wordWrap: "break-word",
    fontSize: "14px",
    lineHeight: "1.4",
  },
  aiMessage: {
    alignSelf: "flex-start",
    backgroundColor: "#e3f2fd",
    color: "#000",
  },
  userMessage: {
    alignSelf: "flex-end",
    backgroundColor: "#2d2d2d",
    color: "#fff",
  },
  inputContainer: {
    display: "flex",
    alignItems: "center",
    backgroundColor: "#fff",
    borderRadius: "30px",
    padding: "10px",
    boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
    width: "85%",
    margin: "20px auto",
    border: "1px solid #ccc",
  },
  input: {
    flex: 1,
    padding: "12px",
    border: "none",
    outline: "none",
    fontSize: "16px",
    backgroundColor: "transparent",
  },
  sendButton: {
    backgroundColor: "#2d2d2d",
    color: "#fff",
    border: "none",
    padding: "12px",
    borderRadius: "50%",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "background 0.2s ease-in-out",
    '&:hover': {
      backgroundColor: "#3d3d3d",
    }
  },
};



export default ChatApp;
