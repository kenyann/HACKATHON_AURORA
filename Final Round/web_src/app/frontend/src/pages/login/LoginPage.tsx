import { AccountInfo, EventType, PublicClientApplication } from "@azure/msal-browser";
import { checkLoggedIn, msalConfig, useLogin } from "../../authConfig";
import { useEffect, useState } from "react";
import { MsalProvider } from "@azure/msal-react";
import { LoginContext } from "../../loginContext";
import Layout from "./Layout_Login";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
    const [loggedIn, setLoggedIn] = useState(false);
    const navigate = useNavigate();
    if (useLogin) {
        var msalInstance = new PublicClientApplication(msalConfig);

        // Default to using the first account if no account is active on page load
        if (!msalInstance.getActiveAccount() && msalInstance.getAllAccounts().length > 0) {
            // Account selection logic is app dependent. Adjust as needed for different use cases.
            msalInstance.setActiveAccount(msalInstance.getActiveAccount());
        }

        // Listen for sign-in event and set active account
        msalInstance.addEventCallback(event => {
            if (event.eventType === EventType.LOGIN_SUCCESS && event.payload) {
                const account = event.payload as AccountInfo;
                msalInstance.setActiveAccount(account);
                setLoggedIn(true);
                navigate("/chat"); // Navigate to chat page after successful login
            }
        });

        useEffect(() => {
            const fetchLoggedIn = async () => {
                setLoggedIn(await checkLoggedIn(msalInstance));
            };

            fetchLoggedIn();
        }, []);

        return (
            <MsalProvider instance={msalInstance}>
                <LoginContext.Provider
                    value={{
                        loggedIn,
                        setLoggedIn
                    }}
                >
                    <Layout />
                </LoginContext.Provider>
            </MsalProvider>
        );
    } else {
        return (
            <LoginContext.Provider
                value={{
                    loggedIn,
                    setLoggedIn
                }}
            >
                <Layout />
            </LoginContext.Provider>
        );
    }
};

export default LoginPage;
