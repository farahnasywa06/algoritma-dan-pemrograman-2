class LinearSearch:

    complexity = "O(n)"

    @staticmethod
    def search(students, keyword):

        keyword = keyword.lower()

        return [
            student
            for student in students
            if (keyword in student.full_name.lower() or keyword in student.nim.lower())
        ]


class SequentialSearch:

    complexity = "O(n)"

    @staticmethod
    def search(students, keyword):

        keyword = keyword.lower()

        results = []

        for student in students:

            if keyword in student.major.lower():

                results.append(student)

        return results


class BinarySearch:

    complexity = "O(log n)"

    @staticmethod
    def search(students, nim):

        students = sorted(students, key=lambda s: s.nim)

        left = 0
        right = len(students) - 1

        while left <= right:

            middle = (left + right) // 2

            if students[middle].nim == nim:

                return [students[middle]]

            if students[middle].nim < nim:

                left = middle + 1

            else:

                right = middle - 1

        return []
