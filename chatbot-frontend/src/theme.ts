import { extendTheme, type ThemeConfig } from '@chakra-ui/react'

const config: ThemeConfig = {
    initialColorMode: 'light',
    useSystemColorMode: true,
}

export const theme = extendTheme({
    config,
    styles: {
        global: {
            body: {
                bg: 'gray.50',
            },
        },
    },
    components: {
        Button: {
            defaultProps: {
                colorScheme: 'blue',
            },
        },
    },
}) 