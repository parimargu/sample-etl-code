import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

interface SearchBarProps {
    onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', gap: 2, mb: 4 }}>
            <TextField
                fullWidth
                variant="outlined"
                placeholder="Search documents..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <Button variant="contained" type="submit" startIcon={<SearchIcon />}>
                Search
            </Button>
        </Box>
    );
};

export default SearchBar;
