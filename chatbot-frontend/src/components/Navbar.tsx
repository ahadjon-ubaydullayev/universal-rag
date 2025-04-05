import React from 'react'
import {
    Box,
    Flex,
    Text,
    IconButton,
    useColorMode,
    useColorModeValue,
    HStack,
} from '@chakra-ui/react'
import { SunIcon, MoonIcon, HamburgerIcon } from '@chakra-ui/icons'

interface NavbarProps {
    onToggleSidebar: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar }) => {
    const { colorMode, toggleColorMode } = useColorMode()
    const bgColor = useColorModeValue('white', 'gray.800')
    const borderColor = useColorModeValue('gray.200', 'gray.700')

    return (
        <Box
            bg={bgColor}
            px={4}
            py={2}
            borderBottom="1px"
            borderColor={borderColor}
            position="sticky"
            top={0}
            zIndex={1}
        >
            <Flex justify="space-between" align="center">
                <HStack spacing={4}>
                    <IconButton
                        aria-label="Toggle Sidebar"
                        icon={<HamburgerIcon />}
                        onClick={onToggleSidebar}
                        display={{ base: 'flex', md: 'none' }}
                    />
                    <Text fontSize="xl" fontWeight="bold">
                        RAG Chatbot
                    </Text>
                </HStack>
                <IconButton
                    aria-label="Toggle color mode"
                    icon={colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
                    onClick={toggleColorMode}
                />
            </Flex>
        </Box>
    )
}

export default Navbar 