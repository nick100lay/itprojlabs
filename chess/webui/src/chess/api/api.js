import axios from "axios";
import { useEffect, useState, useMemo } from "react";

import { getApiUrl } from "./url";


const DEFAULT_TIMEOUT = 5000;


function useApiInitial(endpoint, getParams) {
    const [json, setJson] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        setJson(null);
        setError(null);
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT);
        axios
            .get(getApiUrl(endpoint), {
                signal: controller.signal,
                params: getParams
            })
            .then((resp) => { setJson(resp.data); setError(null); })
            .catch((error) => { setJson(null); setError(error); })
            .finally(() => clearTimeout(timeoutId));
        return () => {
            clearTimeout(timeoutId);
            controller.abort();
        }
    }, [endpoint, getParams]);
    return [json, setJson, error, json === null && error === null];
}


function useApiMethods(endpoint, json, setJson, errors, isLoading, callbacks) {
    return useMemo(() => {
            if (isLoading || errors !== null) {
                return null;
            }
            const methods = {};
            for (let method in callbacks) {
                methods[method] = (newData) => callbacks[method](getApiUrl(endpoint), newData, json, setJson);
            }
            return methods;
        },
        [endpoint, json, setJson, errors, isLoading, callbacks]
    )
}


export function useApi(endpoint, getParams, callbacks) {
    const [json, setJson, errors, isLoading] = useApiInitial(endpoint, getParams);
    const methods = useApiMethods(endpoint, json, setJson, errors, isLoading, callbacks)
    return [json, methods, errors, isLoading, setJson];
} 


function useApiCombinedMethodsMemo(methods1, methods2) {
    return useMemo(() => (
        {...methods1, ...methods2}
    ), [methods1, methods2]);
}


export function useCombinedApiMethods(endpoint, json, methods, errors, isLoading, setJson, callbacks) {
    return useApiCombinedMethodsMemo(
        methods, 
        useApiMethods(endpoint, json, setJson, errors, isLoading, callbacks)
    );
}