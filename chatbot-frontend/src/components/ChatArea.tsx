import React, { useState, useRef, useEffect } from 'react'
import {
  Box,
  VStack,
  HStack,
  Input,
  Button,
  Text,
  Flex,
  useToast,
} from '@chakra-ui/react'
import axios from 'axios'

interface Message {
  text: string
  isUser: boolean
}

const ChatArea = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const toast = useToast()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!input.trim()) return

    const userMessage = input.trim()
    setInput('')
    setMessages(prev => [...prev, { text: userMessage, isUser: true }])
    setIsLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/generate/', {
        question: userMessage
      })

      setMessages(prev => [...prev, { text: response.data.response, isUser: false }])
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to get response from the server',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSendMessage()
    }
  }

  return (
    <Box flex={1} bg="white" borderRadius="lg" boxShadow="sm" display="flex" flexDirection="column">
      <Box flex={1} overflowY="auto" p={4}>
        <VStack spacing={4} align="stretch">
          {messages.map((message, index) => (
            <Flex
              key={index}
              justify={message.isUser ? 'flex-end' : 'flex-start'}
            >
              <Box
                maxW="70%"
                bg={message.isUser ? 'blue.500' : 'gray.100'}
                color={message.isUser ? 'white' : 'black'}
                p={3}
                borderRadius="lg"
                boxShadow="sm"
              >
                <Text>{message.text}</Text>
              </Box>
            </Flex>
          ))}
          {isLoading && (
            <Flex justify="flex-start">
              <Box bg="gray.100" p={3} borderRadius="lg">
                <Text>Thinking...</Text>
              </Box>
            </Flex>
          )}
          <div ref={messagesEndRef} />
        </VStack>
      </Box>
      <Box p={4} borderTop="1px" borderColor="gray.200">
        <HStack>
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <Button
            colorScheme="blue"
            onClick={handleSendMessage}
            isLoading={isLoading}
            disabled={!input.trim() || isLoading}
          >
            Send
          </Button>
        </HStack>
      </Box>
    </Box>
  )
}

export default ChatArea 