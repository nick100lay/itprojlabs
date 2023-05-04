

import { useMemo } from "react"

import { useApi } from "./api"
import { API_ENDPOINTS } from "./url";
import { defaultPostMethod } from "./utils"


function usePlayers() {
    return useApi(API_ENDPOINTS.PLAYERS, undefined, 
        useMemo(() => ({ 
            post: defaultPostMethod
        }), [])
    );
}


export default usePlayers;