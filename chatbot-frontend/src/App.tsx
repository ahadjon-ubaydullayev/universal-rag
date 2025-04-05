import React, { useState } from 'react'
import { ChakraProvider, Box, Flex, Container, ColorModeScript } from '@chakra-ui/react'
import { theme } from './theme'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import { apiService } from './services/api'

interface Message {
    text: string;
    isUser: boolean;
    timestamp: Date;
}

function App() {
    const [messages, setMessages] = useState<Message[]>([])
    const [isSidebarOpen, setIsSidebarOpen] = useState(false)

    const handleQuestionClick = async (question: string) => {
        const userMessage: Message = {
            text: question,
            isUser: true,
            timestamp: new Date(),
        }
        setMessages(prev => [...prev, userMessage])

        try {
            const response = await apiService.generateResponse(question)
            const botMessage: Message = {
                text: response,
                isUser: false,
                timestamp: new Date(),
            }
            setMessages(prev => [...prev, botMessage])
        } catch (error) {
            console.error('Error generating response:', error)
        }
    }

    return (
        <ChakraProvider theme={theme}>
            <ColorModeScript initialColorMode={theme.config.initialColorMode} />
            <Box minH="100vh" bg="gray.50">
                <Navbar onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)} />
                <Container maxW="container.xl" py={4}>
                    <Flex gap={4} h="calc(100vh - 80px)">
                        <Sidebar 
                            onQuestionClick={handleQuestionClick}
                            isOpen={isSidebarOpen}
                            onClose={() => setIsSidebarOpen(false)}
                        />
                        <ChatArea messages={messages} setMessages={setMessages} />
                    </Flex>
                </Container>
            </Box>
        </ChakraProvider>
    )
}

export default App 