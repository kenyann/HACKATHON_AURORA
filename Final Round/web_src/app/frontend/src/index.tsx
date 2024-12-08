import React from "react";
import ReactDOM from "react-dom/client";
import { createHashRouter, RouterProvider } from "react-router-dom";
import { I18nextProvider } from "react-i18next";
import { HelmetProvider } from "react-helmet-async";
import { initializeIcons } from "@fluentui/react";

import "./index.css";

import Chat from "./pages/chat/Chat";
import LayoutWrapper from "./layoutWrapper";
import i18next from "./i18n/config";

import LandingPage from "./pages/login/landingPage";
initializeIcons();

const router = createHashRouter([
    {
        path: "/",
        element: <LandingPage />
    }
    ,
    {
        path: "chat",
        element: <LayoutWrapper />,
        children: [
            {
                index: true,
                // path: "chat",
                element: <Chat />
            },
            // {
            //     path: "qa",
            //     lazy: () => import("./pages/ask/Ask")
            // },
            // {
            //     index: true,
            //     element: <LoginPage />
            // }
        ]
    }
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
    <React.StrictMode>
        <I18nextProvider i18n={i18next}>
            <HelmetProvider>
                <RouterProvider router={router} />
            </HelmetProvider>
        </I18nextProvider>
    </React.StrictMode>
);




// Test
// import React from "react";
// import ReactDOM from "react-dom/client";
// import { RouterProvider, createHashRouter } from "react-router-dom";
// import { LoginProvider, useLoginContext } from "./loginContext_2";
// import { I18nextProvider } from "react-i18next";
// import { HelmetProvider } from "react-helmet-async";
// import { initializeIcons } from "@fluentui/react";

// import "./index.css";

// import Chat from "./pages/chat/Chat";
// import LayoutWrapper from "./layoutWrapper";
// import i18next from "./i18n/config";
// import LoginPage from "./pages/login/LoginPage";
// // import PrivateRoute from "./PrivateRoute";
// import { useRef, useState, useEffect, useContext } from "react";
// // import { useLoginContext } from "./loginContext";

// const AppRoutes: React.FC = () => {
//     const { loggedIn } = useLoginContext();

//     const routes = createHashRouter([
//         {
//             path: "/",
//             element: <LayoutWrapper />,
//             children: [
//                 {
//                     index: true,
//                     element: <Chat />
//                     // element: loggedIn ? <LoginPage /> : <Chat />
//                 }
//                 // ,
//                 // {
//                 //     path: "qa",
//                 //     element: <Chat />
//                 // }
//             ]
//         }
//     ]);

//     return <RouterProvider router={routes} />;
// };

// const rootElement = document.getElementById("root");
// const root = ReactDOM.createRoot(rootElement!);

// root.render(
//     <LoginProvider>
//         <AppRoutes />
//     </LoginProvider>
// );