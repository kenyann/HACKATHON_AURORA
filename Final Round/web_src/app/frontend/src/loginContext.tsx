/**
 * This file defines a context for managing login state in a React application.
 * Context provides a way to pass data through the component tree without having to pass props down manually at every level.
 * For more information, refer to the official React documentation:
 * https://react.dev/learn/passing-data-deeply-with-context
 */

import { createContext } from "react";

export const LoginContext = createContext({
    loggedIn: false,
    setLoggedIn: (_: boolean) => { }
});

// test
// loginContext.tsx
// import React, { createContext, useState, ReactNode } from "react";

// interface LoginContextProps {
//     loggedIn: boolean;
//     setLoggedIn: (loggedIn: boolean) => void;
// }

// interface LoginProviderProps {
//     children: ReactNode;
// }

// const LoginContext = createContext<LoginContextProps | undefined>(undefined);

// export const LoginProvider: React.FC<LoginProviderProps> = ({ children }) => {
//     const [loggedIn, setLoggedIn] = useState(false);

//     return (
//         <LoginContext.Provider value={{ loggedIn, setLoggedIn }}>
//             {children}
//         </LoginContext.Provider>
//     );
// };

// loginContext.tsx
// import React, { createContext, useState, useContext, ReactNode } from "react";

// interface LoginContextProps {
//     loggedIn: boolean;
//     setLoggedIn: (loggedIn: boolean) => void;
// }

// interface LoginProviderProps {
//     children: ReactNode;
// }

// const LoginContext = createContext<LoginContextProps | undefined>(undefined);

// export const LoginProvider: React.FC<LoginProviderProps> = ({ children }) => {
//     const [loggedIn, setLoggedIn] = useState(false);

//     return (
//         <LoginContext.Provider value={{ loggedIn, setLoggedIn }}>
//             {children}
//         </LoginContext.Provider>
//     );
// };

// export const useLoginContext = (): LoginContextProps => {
//     const context = useContext(LoginContext);
//     if (context === undefined) {
//         throw new Error("useLoginContext must be used within a LoginProvider");
//     }
//     return context;
// };