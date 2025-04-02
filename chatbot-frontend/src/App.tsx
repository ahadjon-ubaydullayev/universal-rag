import React, { useState } from 'react'
import { ChakraProvider, Box, Flex, Container } from '@chakra-ui/react'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'

function App() {
  const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([])

  const handleQuestionClick = (question: string) => {
    setMessages(prev => [...prev, { text: question, isUser: true }])
  }

  return (
    <ChakraProvider>
      <Box minH="100vh" bg="gray.50">
        <Navbar />
        <Container maxW="container.xl" py={4}>
          <Flex gap={4} h="calc(100vh - 80px)">
            <Sidebar onQuestionClick={handleQuestionClick} />
            <ChatArea />
          </Flex>
        </Container>
      </Box>
    </ChakraProvider>
  )
}

export default App 