import { ThemeProvider } from "@mui/material";
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider } from "../node_modules/react-router-dom/dist/index"
import Home from "./pages/Home";
import createMuiTheme from "./theme/theme";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Home />} />
    </Route>
  )
);

const App = () => {
  const theme = createMuiTheme() // Passing global styling theme to components.
  return (
    <ThemeProvider theme={theme}>
      <RouterProvider router={router} />
    </ThemeProvider>);
};

export default App;
