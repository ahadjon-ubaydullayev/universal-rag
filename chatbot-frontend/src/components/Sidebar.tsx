import React from 'react'
import { Box, VStack, Button, Text, useToast } from '@chakra-ui/react'

const sampleQuestions = [
  "What are the visiting hours at the hospital?",
  "Who are the cardiology specialists at Harmony Health Center?",
  "What payment options are available at the hospital?"
]

interface SidebarProps {
  onQuestionClick?: (question: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onQuestionClick }) => {
  const toast = useToast()

  const handleQuestionClick = (question: string) => {
    if (onQuestionClick) {
      onQuestionClick(question)
    } else {
      toast({
        title: 'Error',
        description: 'Chat functionality not properly connected',
        status: 'error',
        duration: 3000,
        isClosable: true,
      })
    }
  }

  return (
    <Box w="300px" bg="white" p={4} borderRadius="lg" boxShadow="sm">
      <Text fontWeight="bold" mb={4}>Sample Questions</Text>
      <VStack spacing={2} align="stretch">
        {sampleQuestions.map((question, index) => (
          <Button
            key={index}
            variant="outline"
            size="sm"
            textAlign="left"
            onClick={() => handleQuestionClick(question)}
            whiteSpace="normal"
            height="auto"
            py={2}
          >
            {question}
          </Button>
        ))}
      </VStack>
    </Box>
  )
}

export default Sidebar 