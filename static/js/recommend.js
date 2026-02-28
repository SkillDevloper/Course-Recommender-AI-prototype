/**
 * Recommendations Page JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const queryInput = document.getElementById('queryInput');
    const resultsContainer = document.getElementById('resultsContainer');
    const loadingState = document.getElementById('loadingState');
    const searchInfo = document.getElementById('searchInfo');
    const resultsCount = document.getElementById('resultsCount');
    const currentSearchId = document.getElementById('currentSearchId');
    const currentModelType = document.getElementById('currentModelType');
    
    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const query = queryInput.value.trim();
        const modelType = document.querySelector('input[name="modelType"]:checked').value;
        
        if (!query) {
            appUtils.showNotification('Please enter your learning goals', 'warning');
            queryInput.focus();
            return;
        }
        
        // Show loading state
        loadingState.style.display = 'block';
        resultsContainer.style.display = 'none';
        searchInfo.style.display = 'none';
        
        try {
            const response = await appUtils.makeRequest('/api/recommend', 'POST', {
                query: query,
                model: modelType
            });
            
            if (response.success) {
                displayResults(response);
                appUtils.showNotification(`Found ${response.recommendations.length} recommendations`, 'success');
            }
        } catch (error) {
            console.error('Error getting recommendations:', error);
        } finally {
            loadingState.style.display = 'none';
            resultsContainer.style.display = 'block';
        }
    });
    
    // Display results
    function displayResults(data) {
        resultsCount.textContent = data.recommendations.length;
        currentSearchId.textContent = data.search_id;
        currentModelType.textContent = data.model.toUpperCase();
        currentModelType.className = data.model === 'tfidf' ? 
            'badge bg-primary' : 'badge bg-success';
        
        let html = '';
        
        if (data.recommendations.length === 0) {
            html = `
                <div class="text-center py-5">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">No Courses Found</h4>
                    <p class="text-muted">Try rephrasing your query or using a different model.</p>
                </div>
            `;
        } else {
            data.recommendations.forEach((course, index) => {
                const scoreColor = appUtils.getScoreColor(course.relevance_score);
                const scoreClass = `bg-${scoreColor}`;
                
                html += `
                    <div class="course-card mb-4 p-3">
                        <div class="row">
                            <div class="col-md-9">
                                <div class="d-flex justify-content-between align-items-start mb-2">
                                    <h5 class="mb-0">
                                        ${course.title}
                                        <span class="badge bg-secondary ms-2">${course.course_id}</span>
                                    </h5>
                                    <span class="badge ${scoreClass}">
                                        ${appUtils.formatScore(course.relevance_score)}%
                                    </span>
                                </div>
                                
                                <div class="mb-3">
                                    <span class="badge bg-light text-dark border">
                                        <i class="fas fa-university me-1"></i>
                                        ${course.department}
                                    </span>
                                    <small class="text-muted ms-2">
                                        <i class="fas fa-${course.model === 'tfidf' ? 'key' : 'brain'} me-1"></i>
                                        ${course.model === 'tfidf' ? 'TF-IDF' : 'Neural'} Model
                                    </small>
                                </div>
                                
                                <p class="mb-3">${course.description}</p>
                                
                                <div class="mb-3">
                                    <div class="d-flex align-items-center">
                                        <small class="text-muted me-3">Relevance:</small>
                                        <div class="progress flex-grow-1" style="height: 10px;">
                                            <div class="progress-bar ${scoreClass}" 
                                                 style="width: ${course.relevance_score}%"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="col-md-3">
                                <div class="d-grid gap-2">
                                    <button class="btn btn-outline-primary" 
                                            onclick="saveRecommendation(${data.search_id}, '${course.course_id}')">
                                        <i class="fas fa-bookmark me-2"></i>Save Course
                                    </button>
                                    <button class="btn btn-outline-secondary" 
                                            onclick="showCourseDetails(${index}, '${course.course_id}')">
                                        <i class="fas fa-info-circle me-2"></i>Details
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        
        resultsContainer.innerHTML = html;
        searchInfo.style.display = 'block';
    }
    
    // Set example query
    const exampleQueries = [
        "I want to learn Python for data science and machine learning",
        "Web development with JavaScript and React",
        "Deep learning and neural networks for AI",
        "Data analysis and visualization techniques",
        "Cloud computing and AWS certification"
    ];
    
    // Random example on page load
    queryInput.placeholder = exampleQueries[Math.floor(Math.random() * exampleQueries.length)] + "...";
});

// Save recommendation
async function saveRecommendation(searchId, courseId) {
    try {
        const response = await appUtils.makeRequest('/api/save', 'POST', {
            search_id: searchId,
            course_id: courseId
        });
        
        if (response.success) {
            appUtils.showNotification('Course saved to dashboard!', 'success');
            
            // Disable button
            const button = event.target;
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-check me-2"></i>Saved';
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-success');
        }
    } catch (error) {
        console.error('Error saving recommendation:', error);
    }
}

// Show course details modal
function showCourseDetails(index, courseId) {
    // In a real implementation, this would fetch detailed course information
    const courseTitle = document.querySelectorAll('.course-card h5')[index].textContent;
    
    appUtils.showNotification(`Details for ${courseTitle} would open in a detailed view`, 'info');
}

// Compare models for current query
async function compareModels() {
    const query = document.getElementById('queryInput').value.trim();
    
    if (!query) {
        appUtils.showNotification('Please enter a query first', 'warning');
        return;
    }
    
    try {
        const response = await appUtils.makeRequest(`/api/compare/${encodeURIComponent(query)}`);
        
        if (response.success) {
            // Show comparison in modal or redirect
            window.location.href = `/dashboard#comparison`;
        }
    } catch (error) {
        console.error('Error comparing models:', error);
    }
}

// Make functions available globally
window.saveRecommendation = saveRecommendation;
window.showCourseDetails = showCourseDetails;
window.compareModels = compareModels;