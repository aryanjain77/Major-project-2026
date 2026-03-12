const studyAssistantData = {
  jobs: [
    {
      id: 1,
      title: "Software Developer",
      description: "Builds and maintains software applications and systems",
      avg_salary: "4-15 LPA",
      demand: "Very High",
      skills: [
        {
          name: "Python",
          resources: [
            {
              title: "Python Official Documentation",
              url: "https://www.python.org",
              type: "learning",
              description: "Official Python documentation for learning syntax and libraries"
            },
            {
              title: "LeetCode Python Problems",
              url: "https://leetcode.com/problemset/?topicSlugs=python-3",
              type: "practice",
              description: "Practice Python coding problems to improve algorithmic skills"
            }
          ]
        },
        { name: "JavaScript", resources: [] },
        { name: "Git", resources: [] }
      ]
    },
    {
      id: 2,
      title: "Data Scientist",
      description: "Analyzes data to derive business insights",
      avg_salary: "6-20 LPA",
      demand: "High",
      skills: [
        {
          name: "Python",
          resources: [
            {
              title: "Coursera: Python for Data Science",
              url: "https://www.coursera.org/learn/python-for-data-science",
              type: "learning",
              description: "Comprehensive course on Python for data analysis"
            },
            {
              title: "Kaggle Datasets",
              url: "https://www.kaggle.com/datasets",
              type: "practice",
              description: "Practice data analysis with real-world datasets"
            }
          ]
        },
        { name: "Statistics", resources: [] },
        { name: "Machine Learning", resources: [] }
      ]
    },
    {
      id: 3,
      title: "Product Manager",
      description: "Defines product strategy and roadmap",
      avg_salary: "8-25 LPA",
      demand: "High",
      skills: [
        {
          name: "Product Strategy",
          resources: [
            {
              title: "Coursera: Product Management Fundamentals",
              url: "https://www.coursera.org/learn/product-management",
              type: "learning",
              description: "Learn product management principles and frameworks"
            },
            {
              title: "Product School Resources",
              url: "https://www.productschool.com/resources",
              type: "learning",
              description: "Free resources for product management skills"
            }
          ]
        },
        { name: "Agile Methodology", resources: [] }
      ]
    },
    {
      id: 4,
      title: "UI/UX Designer",
      description: "Designs user interfaces and experiences",
      avg_salary: "4-12 LPA",
      demand: "High",
      skills: [
        {
          name: "Figma",
          resources: [
            {
              title: "Figma Official Tutorials",
              url: "https://www.figma.com/resources/learn-design/",
              type: "learning",
              description: "Official Figma tutorials for UI/UX design"
            },
            {
              title: "Dribbble UI Design Inspiration",
              url: "https://dribbble.com/tags/ui-design",
              type: "practice",
              description: "Explore UI design ideas to practice design skills"
            }
          ]
        },
        { name: "User Research", resources: [] }
      ]
    },
    {
      id: 5,
      title: "Cloud Engineer",
      description: "Manages cloud infrastructure and services",
      avg_salary: "6-18 LPA",
      demand: "High",
      skills: [
        {
          name: "AWS",
          resources: [
            {
              title: "AWS Training and Certification",
              url: "https://aws.amazon.com/training/",
              type: "learning",
              description: "Official AWS training for cloud computing skills"
            },
            {
              title: "AWS Skill Builder",
              url: "https://skillbuilder.aws/",
              type: "practice",
              description: "Hands-on labs for AWS cloud practice"
            }
          ]
        },
        { name: "Docker", resources: [] }
      ]
    }
  ]
};

export default studyAssistantData;