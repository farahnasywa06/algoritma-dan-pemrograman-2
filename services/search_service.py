class LinearSearch:

    complexity = "O(n)"

    @staticmethod
    def search(students, keyword, field="full_name"):

        keyword = str(keyword).lower()

        results = []

        for student in students:

            value = str(getattr(student, field, "")).lower()

            if keyword in value:

                results.append(student)

        return results


class SequentialSearch:

    complexity = "O(n)"

    @staticmethod
    def search(students, keyword, field="full_name"):
        keyword = str(keyword).lower()

        results = []

        for student in students:

            value = str(getattr(student, field, "")).lower()

            if keyword in value:

                results.append(student)

        return results


class BinarySearch:

    complexity = "O(log n)"

    @staticmethod
    def search(students, keyword, field="nim"):

        keyword = str(keyword)

        students = sorted(students, key=lambda s: str(getattr(s, field)))

        left = 0
        right = len(students) - 1

        while left <= right:

            middle = (left + right) // 2

            current = str(getattr(students[middle], field))

            if current == keyword:

                return [students[middle]]

            elif current < keyword:

                left = middle + 1

            else:

                right = middle - 1

        return []
