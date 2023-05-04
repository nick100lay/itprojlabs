
import { useMemo } from "react"
import axios from "axios"

import { useApi, useCombinedApiMethods } from "./api"
import { API_ENDPOINTS } from "./url";
import { defaultPostMethod } from "./utils"


function useCurrentMatches() {
    const [ matches, methods, errors, isLoading, setMatches ] = useApi(API_ENDPOINTS.CURRENT_MATCHES, undefined,
        useMemo(() => ({ 
            post: defaultPostMethod
        }), [])
    );

    const newMethods = useCombinedApiMethods(API_ENDPOINTS.COMPLETED_MATCHES, matches, methods, errors, isLoading, setMatches,
        useMemo(() => ({
            postResults: (url, newResults, matches, setMatches) => (
                axios
                    .post(url, newResults)
                    .then((resp) => {
                        const hist = {};
                        resp.data.forEach(match => hist[match.id] = true);
                        setMatches(matches.filter(match => !hist[match.id]))
                    })
            )
        }), [])
    );

    return [ matches, newMethods, errors, isLoading, setMatches ];
}


export default useCurrentMatches;