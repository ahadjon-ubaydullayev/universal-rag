import React from 'react'
import {
    Box,
    VStack,
    Button,
    Text,
    useColorModeValue,
    Drawer,
    DrawerContent,
    DrawerOverlay,
    DrawerCloseButton,
    DrawerHeader,
    DrawerBody,
} from '@chakra-ui/react'
import { config } from '../config'

interface SidebarProps {
    onQuestionClick: (question: string) => void;
    isOpen: boolean;
    onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onQuestionClick, isOpen, onClose }) => {
    const bgColor = useColorModeValue('white', 'gray.800')
    const hoverBg = useColorModeValue('gray.100', 'gray.700')
    const borderColor = useColorModeValue('gray.200', 'gray.700')

    const sidebarContent = (
        <VStack spacing={2} align="stretch" p={4}>
            <Text fontSize="lg" fontWeight="bold" mb={2}>
                Sample Questions
            </Text>
            {config.DEFAULT_QUESTIONS.map((question, index) => (
                <Button
                    key={index}
                    variant="ghost"
                    justifyContent="flex-start"
                    onClick={() => {
                        onQuestionClick(question)
                        onClose()
                    }}
                    _hover={{ bg: hoverBg }}
                    whiteSpace="normal"
                    height="auto"
                    py={2}
                    px={4}
                    textAlign="left"
                    wordBreak="break-word"
                >
                    {question}
                </Button>
            ))}
        </VStack>
    )

    return (
        <>
            {/* Desktop Sidebar */}
            <Box
                display={{ base: 'none', md: 'block' }}
                w="300px"
                h="100%"
                bg={bgColor}
                borderRight="1px"
                borderColor={borderColor}
                position="sticky"
                top="0"
                overflowY="auto"
            >
                {sidebarContent}
            </Box>

            {/* Mobile Drawer */}
            <Drawer
                isOpen={isOpen}
                placement="left"
                onClose={onClose}
                size="full"
            >
                <DrawerOverlay />
                <DrawerContent>
                    <DrawerCloseButton />
                    <DrawerHeader>Sample Questions</DrawerHeader>
                    <DrawerBody>
                        {sidebarContent}
                    </DrawerBody>
                </DrawerContent>
            </Drawer>
        </>
    )
}

export default Sidebar 