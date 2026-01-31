import { useEffect, useState } from "react";
import apiClient from "../api/client";

export const useGetTransactions = (year, month) => {
    const [transactions, setTransactions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchTransactions = async () => {
        setLoading(true);
        setError(null);
        try {
            const apiResponse = await apiClient.get("/transactions", {
                params: { year, month },
            });
            const data = apiResponse?.data?.transactions;
            setTransactions(data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTransactions();
    }, [year, month]);

    return {
        transactions,
        transactionsIsLoading: loading,
        transactionsIsErrored: error,
        refetchTransactions: fetchTransactions,
    };
};
