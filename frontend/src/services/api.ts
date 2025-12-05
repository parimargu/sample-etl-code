import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SearchResult {
  chunk_id: string;
  doc_id: string;
  text: string;
  score: number;
}

export interface Document {
  doc_id: string;
  text: string;
}

export const searchDocuments = async (query: string): Promise<SearchResult[]> => {
  constresponse = await api.post<SearchResult[]>('/search', { query });
  return response.data;
};

export const getDocument = async (docId: string): Promise<Document> => {
  const response = await api.get<Document>(`/document/${docId}`);
  return response.data;
};
