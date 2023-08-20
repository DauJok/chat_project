import { createTheme } from "@mui/material";
// Used to define global styling used throughout the project.

declare module "@mui/material/styles" {
    interface Theme {
        primaryAppBar: {
            height: number;
        };
    }
    interface ThemeOptions {
        primaryAppBar?: { // Optional if there is a question mark.
            height?: number;
        };
    }
}

export const createMuiTheme = () => {
    let theme = createTheme({
        primaryAppBar: {
            height: 50,
        },
        components: {
            MuiAppBar: {
                defaultProps: {
                    color: "default",
                    elevation: 0,
                }
            }
        }
    });
    return theme;
};

export default createMuiTheme;