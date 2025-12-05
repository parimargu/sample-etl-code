import React, { useState } from 'react';
import { Container, Typography, CssBaseline, Box } from '@mui/material';
import SearchBar from './components/SearchBar';
import ResultsGrid from './components/ResultsGrid';
import DocumentViewer from './components/DocumentViewer';
import { searchDocuments, getDocument, SearchResult, Document } from './services/api';

function App() {
    const [results, setResults] = useState<SearchResult[]>([]);
    const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
    const [viewerOpen, setViewerOpen] = useState(false);
    const [loadingDoc, setLoadingDoc] = useState(false);

    const handleSearch = async (query: string) => {
        try {
            const data = await searchDocuments(query);
            setResults(data);
        } catch (error) {
            console.error("Search failed:", error);
        }
    };

    const handleResultClick = async (docId: string) => {
        setViewerOpen(true);
        setLoadingDoc(true);
        try {
            const doc = await getDocument(docId);
            setSelectedDoc(doc);
        } catch (error) {
            console.error("Failed to fetch document:", error);
        } finally {
            setLoadingDoc(false);
        }
    };

    return (
        <React.Fragment>
            <CssBaseline />
            <Container maxWidth="lg" sx={{ py: 4 }}>
                <Typography variant="h3" component="h1" gutterBottom align="center">
                    NLP Document Search
                </Typography>

                <SearchBar onSearch={handleSearch} />

                <Box sx={{ mt: 4 }}>
                    <ResultsGrid results={results} onResultClick={handleResultClick} />
                </Box>

                <DocumentViewer
                    open={viewerOpen}
                    onClose={() => setViewerOpen(false)}
                    document={selectedDoc}
                    loading={loadingDoc}
                />
            </Container>
        </React.Fragment>
    );
}

export default App;
