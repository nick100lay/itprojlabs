
import { useMemo } from "react"

import { useApi } from "./api"
import { API_ENDPOINTS } from "./url";


function useCompletedMatches() {
    return useApi(API_ENDPOINTS.COMPLETED_MATCHES, undefined,
        useMemo(() => ({}), [])
    );
}


export default useCompletedMatches;