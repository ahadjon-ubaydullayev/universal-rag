import React from 'react'
import { Box, Heading, Container } from '@chakra-ui/react'

const Navbar = () => {
  return (
    <Box bg="blue.500" color="white" py={4}>
      <Container maxW="container.xl">
        <Heading size="md">RAG Chatbot</Heading>
      </Container>
    </Box>
  )
}

export default Navbar 