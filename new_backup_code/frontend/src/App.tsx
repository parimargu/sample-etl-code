import React, { useState } from 'react';
import { Container, Typography, CssBaseline, Box } from '@mui/material';
import SearchBar from './components/SearchBar';
import ResultsGrid from './components/ResultsGrid';
import DocumentViewer from './components/DocumentViewer';
import LoadingOverlay from './components/LoadingOverlay';
import { searchDocuments, getDocument, SearchResult, Document } from './services/api';

function App() {
    const [results, setResults] = useState<SearchResult[]>([]);
    const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
    const [viewerOpen, setViewerOpen] = useState(false);
    const [loadingDoc, setLoadingDoc] = useState(false);
    const [searching, setSearching] = useState(false);

    const handleSearch = async (query: string) => {
        setSearching(true);
        try {
            // Artificial delay to show the beautiful loader
            await new Promise(resolve => setTimeout(resolve, 800));
            const data = await searchDocuments(query);
            setResults(data);
        } catch (error) {
            console.error("Search failed:", error);
        } finally {
            setSearching(false);
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
            <Box sx={{
                minHeight: '100vh',
                background: 'linear-gradient(180deg, #f8f9fa 0%, #eef2ff 100%)',
                pt: 8,
                pb: 8
            }}>
                <Container maxWidth="lg">
                    <Box sx={{ mb: 8, textAlign: 'center' }}>
                        <Typography variant="h3" component="h1" gutterBottom sx={{ mb: 2 }}>
                            NLP Document Search
                        </Typography>
                        <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto', mb: 4 }}>
                            Intelligent semantic search powered by advanced NLP embeddings.
                            Find exactly what you're looking for.
                        </Typography>
                        <SearchBar onSearch={handleSearch} />
                    </Box>

                    <Box sx={{ mt: 4 }}>
                        <ResultsGrid results={results} onResultClick={handleResultClick} />
                    </Box>

                    <DocumentViewer
                        open={viewerOpen}
                        onClose={() => setViewerOpen(false)}
                        document={selectedDoc}
                        loading={loadingDoc}
                    />

                    <LoadingOverlay open={searching} message="Analyzing documents..." />
                </Container>
            </Box>
        </React.Fragment>
    );
}

export default App;
