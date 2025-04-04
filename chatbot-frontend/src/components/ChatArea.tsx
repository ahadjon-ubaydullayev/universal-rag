import React, { useRef, useEffect } from 'react'
import {
  Box,
  VStack,
  HStack,
  Input,
  Button,
  Text,
  useToast,
  Spinner,
  useColorModeValue,
  Flex,
} from '@chakra-ui/react'
import ReactMarkdown from 'react-markdown'
import { apiService } from '../services/api'
import { config } from '../config'

interface Message {
  text: string
  isUser: boolean
  timestamp: Date
}

interface ChatAreaProps {
  messages: Message[]
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
}

const ChatArea: React.FC<ChatAreaProps> = ({ messages, setMessages }) => {
  const [input, setInput] = React.useState('')
  const [isLoading, setIsLoading] = React.useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const toast = useToast()

  const bgColor = useColorModeValue('white', 'gray.800')
  const userMessageBg = useColorModeValue('blue.100', 'blue.900')
  const botMessageBg = useColorModeValue('gray.100', 'gray.700')
  const borderColor = useColorModeValue('gray.200', 'gray.600')

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      text: input.trim(),
      isUser: true,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await apiService.generateResponse(input.trim())
      const botMessage: Message = {
        text: response,
        isUser: false,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : config.DEFAULT_ERROR_MESSAGE
      toast({
        title: 'Error',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <Box
      flex={1}
      bg={bgColor}
      borderRadius="lg"
      boxShadow="sm"
      display="flex"
      flexDirection="column"
    >
      <Box flex={1} overflowY="auto" p={4}>
        <VStack spacing={4} align="stretch">
          {messages.map((message, index) => (
            <Flex
              key={index}
              justify={message.isUser ? 'flex-end' : 'flex-start'}
            >
              <Box
                maxW="80%"
                bg={message.isUser ? userMessageBg : botMessageBg}
                p={3}
                borderRadius="lg"
                boxShadow="sm"
              >
                {message.isUser ? (
                  <Text>{message.text}</Text>
                ) : (
                  <ReactMarkdown>{message.text}</ReactMarkdown>
                )}
                <Text
                  fontSize="xs"
                  color="gray.500"
                  mt={1}
                  textAlign="right"
                >
                  {message.timestamp.toLocaleTimeString()}
                </Text>
              </Box>
            </Flex>
          ))}
          {isLoading && (
            <Flex justify="flex-start">
              <Box
                bg={botMessageBg}
                p={3}
                borderRadius="lg"
                boxShadow="sm"
              >
                <HStack>
                  <Spinner size="sm" />
                  <Text>Thinking...</Text>
                </HStack>
              </Box>
            </Flex>
          )}
          <div ref={messagesEndRef} />
        </VStack>
      </Box>
      <Box p={4} borderTop="1px" borderColor={borderColor}>
        <HStack>
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
            maxLength={config.MAX_MESSAGE_LENGTH}
          />
          <Button
            colorScheme="blue"
            onClick={handleSend}
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