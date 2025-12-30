import { useEffect, useState } from "react"
import apiClient from "../api/client"

export const useGetTransactions = () => {
    const [transactions, setTransactions] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const fetchTransactions = async () => {
        setLoading(true)
        setError(null)
        try {
            const apiResponse = await apiClient.get('/transactions')
            const data= apiResponse?.data?.transactions
            setTransactions(data)
        } catch  (error){
            setError(error.message)
        }finally{
            setLoading(false)
        }
    }

    useEffect(()=> {
        fetchTransactions()
    }, [])

    return {
        transactions,
        transactionsIsLoading: loading,
        transactionsIsErrored: error
    }
}