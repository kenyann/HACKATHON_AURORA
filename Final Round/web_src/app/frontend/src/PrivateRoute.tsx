// // PrivateRoute.tsx
// import React, { useContext } from "react";
// import { Navigate } from "react-router-dom";
// import { LoginContext } from "./loginContext";

// const PrivateRoute: React.FC<{ element: React.ReactElement }> = ({ element }) => {
//     const { loggedIn } = useContext(LoginContext);

//     return loggedIn ? element : <Navigate to="/" />;
// };

// export default PrivateRoute;